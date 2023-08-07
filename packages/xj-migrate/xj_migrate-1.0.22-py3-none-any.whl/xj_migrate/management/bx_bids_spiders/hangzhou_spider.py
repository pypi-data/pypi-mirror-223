# encoding: utf-8
"""
@project: djangoModel->hangzhou_spider
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 杭州市的爬取文件
@created_time: 2023/5/4 12:15
"""
import datetime
import logging
import os
from time import sleep

from lxml import etree
import requests
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER

from config.config import JConfig
from xj_migrate.services.excel_export_service import ExcelExport
from xj_migrate.utils.custom_tool import write_to_log
from ..spider_base import SpiderBase

LOGGER.setLevel(logging.ERROR)

main_config = JConfig()


class HanZhouSpider(SpiderBase):
    key = "HangZhou"  # 该爬虫类的搜索key
    url = "https://ggzy.hzctc.hangzhou.gov.cn/SecondPage/ProjectAfficheList?title=&area=&afficheType=22"  # 爬取的入口链接地址
    header = {
        "Host": "ggzy.hzctc.hangzhou.gov.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68",
    }

    save_path = main_config.get_base_dir() + "/resource_files/spider/" + datetime.date.today().strftime('%y%m%d') + "/"  # 保存的文件地址
    save_file_name = datetime.date.today().strftime('%y%m%d') + key + ".xls"  # 保存的文件名
    heartbeat = -1  # 爬取的频率是否需要定时暂定频率，单位为秒。非强制字段属性

    def __init__(self):
        """外层调用方面请做好"""
        if not self.save_path:
            raise Exception("没有找到爬取文件的保存路径")
        # request会话对象初始化
        self.session = requests.session()
        # 浏览器初始化
        chrome_options = webdriver.Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 实现了规避监测
        self.browser = webdriver.WebDriver(options=chrome_options)
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)

    def get_links(self):
        """
        如果是需要再二级页面获取信息则需要进行先获取链接点击
        :return:
        """
        self.browser.get(self.url)
        sleep(3)
        links = []
        try:
            for i in self.browser.find_elements(by=By.XPATH, value="//tbody/tr/td/a"):
                links.append(i.get_attribute("href").replace("undefined", "17"))
            self.browser.close()
        except Exception as e:
            print("错误捕捉：", str(e))
        return links

    def get_detail(self, link):
        response = self.session.get(url=link, headers=self.header)
        return response.text

    def node_select(self, response_html=None):
        """
        节点选择,xpath,ID,Class等等
        必须继承并且重写该方法
        :return:
        """
        if not response_html:
            return {}
        node_dict = {}
        # 网页写入本地
        # with open("D:\\tempMaterial\\desktop\download.html", "w", encoding="utf-8") as fp:
        #     fp.write(response_html)
        info_html = etree.HTML(response_html)
        title_xpath = "//div[@class='MainList']//div[@class='WordSection1']/div[1]//tr[1]/td[2]/p[@class='MsoNormal']//span/text()"
        title = info_html.xpath(title_xpath)
        node_dict["title"] = title[0] if title and isinstance(title, list) else title
        if not node_dict["title"]:
            return None
        return node_dict

    def run(self):
        """
        执行爬虫的方法，其他自定义获取
        必须继承并且重写该方法
        :return:
        """
        links = self.get_links()
        save_dict_list = []
        for link in links[1:]:
            html_str = self.get_detail(link)
            detail_info = self.node_select(html_str)
            if not detail_info:
                continue
            save_dict_list.append(detail_info)
        print("save_dict_list:", save_dict_list)
        return self.save(save_dict_list=save_dict_list)

    def save(self, save_dict_list=None):
        """
        将爬取的文件保存到excel或者csv文件里面
        统一使用数据库迁移迁移导入数据库
        :return:
        """
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        if not save_dict_list:
            return

        try:
            export_instance = ExcelExport()
            data, err = export_instance.only_write(input_dict_list=save_dict_list)
            return export_instance.save(workbook=export_instance.only_write_wb, save_path=self.save_path)
        except Exception as e:
            write_to_log(err_obj=e)
