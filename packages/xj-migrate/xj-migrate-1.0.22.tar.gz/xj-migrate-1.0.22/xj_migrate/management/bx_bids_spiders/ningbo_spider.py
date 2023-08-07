# encoding: utf-8
"""
@project: djangoModel->hangzhou_spider
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 杭州市的爬取文件
@created_time: 2023/5/4 12:15
"""
import logging
import re
import time

from lxml import etree
import requests
from selenium.webdriver.remote.remote_connection import LOGGER

from main.settings import BASE_DIR
from xj_migrate.utils.custom_tool import dynamic_load_class
from ..spider_base import SpiderBase

LOGGER.setLevel(logging.ERROR)


class NingBoSpider(SpiderBase):
    # 该爬虫类的搜索key
    key = "WenZhou"
    url = "http://ggzy.zwb.ningbo.gov.cn/cms/gcjszbggn/index_{}.htm"  # 爬取的入口链接地址
    header = {
        "Host": "ggzy.zwb.ningbo.gov.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68",
    }
    start_page = 1
    end_page = 2

    # 代理账号密码
    username = "t18731357743290"
    password = "kg2fc4ca"
    proxies = {"http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": "e604.kdltps.com:15818"}}

    # 资源转存路由以及请求头部
    # upload_url = "https://bid-beta.hhmore.cn/api/resource/upload_file"
    upload_url = "https://bid-online.hhmore.cn/api/resource/upload_file"
    upload_headers = {
        'Content-Length': '<calculated when request is sent>',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50IjoiZ2FvZHQiLCJ1c2VyX2lkIjoxMSwicGxhdGZvcm1faWQiOjUsInBsYXRmb3JtX2NvZGUiOiJCSURPTkxJTkUiLCJleHAiOjE2OTAxODkwMjh9.5AeBiBKPhOEHzvx9gRuxIPYnhg7yy09iF88tRAX4E3U'
    }

    def __init__(self):
        """外层调用方面请做好"""
        self.session = requests.session()

    def loop_request(self, url=None, request_times=0, max_request_times=15):
        while request_times <= max_request_times:
            try:
                response = self.session.get(
                    url=url,
                    headers=self.header,
                    timeout=50,
                    proxies=self.proxies
                )
                if response and response.status_code == 200:
                    return response
            except requests.exceptions.ProxyError:
                continue
            request_times += 1
            print("请求：%s，请求失败%d次" % (url, request_times))
        return None

    def get_links(self, start_page=1, end_page=2):
        """
        如果是需要再二级页面获取信息则需要进行先获取链接点击
        :return:
        """
        links = []
        for page in range(start_page, end_page):
            try:
                current_url = self.url.format(str(page))
                response = self.loop_request(url=current_url)
                if not response:
                    continue
                link_html = etree.HTML(response.text)
                current_page_links = link_html.xpath("//ul/div[@class='c1-body']/li/a/@href")
                links += current_page_links
            except Exception as e:
                continue
        return links

    def node_select(self, response_html=None):
        """
        节点选择,xpath,ID,Class等等
        必须继承并且重写该方法
        :return:
        """
        if not response_html:
            return {}
        node_dict = {}
        info_html = etree.HTML(response_html)

        # ------------------------- section 解析html获取信息 start -------------------------------------
        # 行政区划编码
        node_dict["region_code"] = "330200000000"
        # 编码
        node_dict["category_id"] = 107
        node_dict["classify_id"] = 52
        node_dict["user_id"] = 1
        node_dict["show_photo"] = 0

        # 标题
        title = info_html.xpath("//div[@class='frameNews']/h4/text()")
        node_dict["title"] = title[0] if title and isinstance(title, list) else title

        # 项目简介 ==>> 信息表的内容
        content = info_html.xpath("//div[@class='column noBox']/div[@class='frameNews']")
        content_str = etree.tostring(content[0], encoding='utf-8', pretty_print=True, method='html').decode('utf-8') if content and isinstance(content, list) else content or ""
        # 去除js内容
        node_dict["content"] = re.sub(r'<script[\s\S]*</script>', "", content_str)

        images_src = info_html.xpath("//div[@class='column noBox']/div[@class='frameNews']//img/@src")
        # 如果内容有图片则处理数据并返回
        if images_src:
            # print("content === ", node_dict["content"])
            print("image_src === ", images_src[0])
            node_dict["show_photo"] = 1
            image_rep = requests.get(images_src[0]).content
            image_path = str(BASE_DIR) + "/resource_files/download/" + str(time.time_ns()) + ".jpeg"
            with open(image_path, 'wb') as f:
                f.write(image_rep)

            # 需要注意的是Content-Length参数如果没有，data表单则不会随着请求被发送给服务端，且使用fiddler抓包的过程中，也无法看到data表单
            file = {'file': open(image_path, 'rb')}
            result = requests.post(self.upload_url, headers=self.upload_headers, data=None, files=file).json()
            new_image_url = result["data"]["url"]
            print("upload success === ", result["data"]["url"])
            node_dict["content"] = "<img class=\"bx_information_images\"  src=\"" + new_image_url + "\" alt=\"公告正文\">"
            return node_dict

        # 招标编码
        node_dict["bid_number"] = ""

        # 招标单位
        invite_bid_unit = info_html.xpath("//div[@class='column noBox']/div[@class='frameNews']/div[2]/p[15]/text()")
        node_dict["invite_bid_company"] = invite_bid_unit[0] if isinstance(invite_bid_unit, list) and len(invite_bid_unit) > 0 else invite_bid_unit or "无"

        # 招标联系人
        invite_contact_person = info_html.xpath("//div[@class='column noBox']/div[@class='frameNews']/div[2]/p[17]/text()")
        node_dict["invite_contact"] = invite_contact_person[0] if isinstance(invite_contact_person, list) and len(invite_contact_person) >= 1 else invite_contact_person or "无"

        # 招标联系电话
        invite_contact_phone = info_html.xpath("//div[@class='column noBox']/div[@class='frameNews']/div[2]/p[18]/text()")
        node_dict["invite_contact_number"] = invite_contact_phone[0] if isinstance(invite_contact_phone, list) and len(invite_contact_phone) >= 1 else invite_contact_phone or "无"

        # 代理单位
        agent_bid_unit = info_html.xpath("//div[@class='column noBox']/div[@class='frameNews']/div[2]/p[20]/text()")
        node_dict["agent_company"] = agent_bid_unit[0] if isinstance(agent_bid_unit, list) and len(agent_bid_unit) >= 1 else agent_bid_unit or "无"
        node_dict["agent_company"] = node_dict["agent_company"].replace("招 标 代 理 机 构：", "")

        # 代理联系人
        agent_contact_person = info_html.xpath("//div[@class='column noBox']/div[@class='frameNews']/div[2]/p[22]/text()")
        node_dict["agent_contact"] = agent_contact_person[0] if isinstance(agent_contact_person, list) and len(agent_contact_person) >= 1 else agent_contact_person or "无"

        # 代理联系电话
        agent_contact_phone = info_html.xpath("//div[@class='column noBox']/div[@class='frameNews']/div[2]/p[23]/text()")
        node_dict["agent_contact_number"] = agent_contact_phone[0] if isinstance(agent_contact_phone, list) and len(agent_contact_phone) >= 1 else agent_contact_phone or "无"

        # ------------------------- section 解析html获取信息 end   -------------------------------------
        if not node_dict["title"]:
            return None
        return node_dict

    def run(self):
        """
        执行爬虫的方法，其他自定义获取
        必须继承并且重写该方法
        :return:
        """
        links = self.get_links(start_page=self.start_page, end_page=self.end_page)
        # links = {"/cms/gcjszbggn/204956.htm"}
        for link in links:
            response = self.loop_request(url="http://ggzy.zwb.ningbo.gov.cn" + str(link))
            if response and not response.status_code == 200:
                continue

            detail_info = self.node_select(response.text)

            if not detail_info:
                continue
            self.save(detail_info=detail_info)

    def save(self, *args, detail_info, **kwargs):
        ThreadItemService, err = dynamic_load_class(import_path="xj_thread.services.thread_item_service", class_name="ThreadItemService")
        if err:
            raise Exception(err)

        Thread, err = dynamic_load_class(import_path="xj_thread.models", class_name="Thread")
        if err:
            raise Exception(err)
        if not Thread.objects.filter(title=detail_info.get("title")).first():
            data, err = ThreadItemService.add(params=detail_info)
            print("插入结果", data, "err:", err)
        else:
            # Thread.objects.filter(title=detail_info.get("title")).delete()
            # data, err = ThreadItemService.add(params=detail_info)
            # print("已插入，重新覆盖", data)
            print("已插入，跳过插入")
