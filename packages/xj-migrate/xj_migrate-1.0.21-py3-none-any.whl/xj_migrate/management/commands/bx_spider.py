# encoding: utf-8
"""
@project: djangoModel->migrate_by_spider
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 镖行业务流程爬取数据
@created_time: 2023/5/4 11:19
"""

from django.core.management.base import BaseCommand

from xj_migrate.management.bx_bids_spiders.hangzhou_spider import HanZhouSpider
from xj_migrate.management.bx_bids_spiders.ningbo_spider import NingBoSpider
from xj_migrate.utils.custom_tool import write_to_log


# note 待完成脚本的爬取的网站
# "NingBo": "http://ggzy.zwb.ningbo.gov.cn/cms/jyxxgcjs/index.htm",
# "JiaXing": "http://hn.jxzbtb.cn/jygg/003001/subpagesecond.html",
# "HuiZhou": "http://ggzyjy.huzhou.gov.cn/",
# "ShaoXing": "http://ol.ggb.sx.gov.cn/jsgc/001001/sec.html",
# "JinHua": "http://ggzyjy.jinhua.gov.cn/col/col1229641554/index.html",
# "XuZhou": "https://ggzy.qz.gov.cn/col/col1229683626/index.html?number=ggjyA004",
# "ZhouShan": "http://zsztb.zhoushan.gov.cn/col/col1229679798/index.html?key",
# "TaiZhou": "https://tzztb.zjtz.gov.cn/tzcms/gcjy/index.htm",
# "LiShui": "https://lssggzy.lishui.gov.cn/"


class Command(BaseCommand):
    # 帮助文本, 一般备注命令的用途及如何使用。
    help = "爬取招投标咨询,并保存到文件中"

    spider_city_instance = {
        # "HangZhou": HanZhouSpider,
        "WenZhou": NingBoSpider
    }

    # 给命令添加一个名为name的参数
    def add_arguments(self, parser):
        pass

    # 核心业务逻辑，通过options字典接收name参数值，拼接字符串后输出
    def handle(self, *args, **options):
        for key, instance in self.spider_city_instance.items():
            try:
                instance().run()
            except Exception as e:
                write_to_log(prefix="打印日志系統叫脚本", err_obj=e)
