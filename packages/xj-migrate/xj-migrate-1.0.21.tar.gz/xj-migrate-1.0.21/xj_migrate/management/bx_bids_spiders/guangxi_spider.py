import json
import time

import requests

# 定义URL和基本头信息

url = "http://zfcg.gxzf.gov.cn/portal/category"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
session = requests.session()
response = session.get(
    url="http://zfcg.gxzf.gov.cn/luban/category?parentId=66485&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-38919.959-pc-websitegroup-navBar-front.5.31c38200252811ee9fc705d0d1d3a19f",
    headers=headers
)

# 发送GET请求并获取响应内容
print(int(round(time.time()) * 1000))
res = session.post(
    url=url,
    data=json.dumps({
        "pageNo": 1,
        "pageSize": 15,
        "categoryCode": "ZcyAnnouncement1",
        "_t": int(round(time.time()) * 1000)
    }),
    headers={
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "114",
        "Content-Type": "application/json",
        "Cookie": "_zcy_log_client_uuid=794d2b10-26c4-11ee-891c-fd7e92367e17; acw_tc=ac11000116898394034482853e243b04a5f9f72c6f3ea500a0ba63402f0983",
        "Host": "zfcg.gxzf.gov.cn",
        "Origin": "http://zfcg.gxzf.gov.cn",
        "Pragma": "no-cache",
        "Referer": "http://zfcg.gxzf.gov.cn/luban/category?parentId=66485&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-38919.959-pc-websitegroup-navBar-front.5.31c38200252811ee9fc705d0d1d3a19f",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
        "X-Requested-With": "XMLHttpRequest"
    },
    # proxies={"http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": "t18731357743290", "pwd": "kg2fc4ca", "proxy": "e604.kdltps.com:15818"}}
)
print("res:", res)
print(res.text)
