# encoding: utf-8
"""
@project: djangoModel->spier_base
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 所有爬虫抽象类
@created_time: 2023/5/4 12:16
"""
from abc import ABCMeta, abstractmethod


class SpiderBase(metaclass=ABCMeta):
    key = ""  # 该爬虫类的搜索key
    url = ""  # 爬取的入口链接地址
    save_path = ""  # 保存的文件地址
    heartbeat = -1  # 爬取的频率是否需要定时暂定频率，单位为秒

    def get_links(self, *args, **kwargs):
        """
        如果是需要再二级页面获取信息则需要进行先获取链接点击
        :return:
        """
        pass

    def get_detail(self, *args, **kwargs):
        """
        获取详细信息
        :return:
        """
        pass

    @abstractmethod
    def node_select(self, *args, **kwargs):
        """
        节点选择,xpath,ID,Class，jsonpath等等
        必须继承并且重写该方法
        :return:
        """
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        执行爬虫的方法，其他自定义获取
        必须继承并且重写该方法
        :return:
        """
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        """
        将爬取的文件保存到excel或者csv文件里面
        统一使用数据库迁移迁移导入数据库
        :return:
        """
        pass
