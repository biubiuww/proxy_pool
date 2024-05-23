# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import re
import json
from time import sleep

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        """
        start_url = "https://www.zdaye.com/dayProxy.html"
        html_tree = WebRequest().get(start_url, verify=False).tree
        latest_page_time = html_tree.xpath("//span[@class='thread_time_info']/text()")[0].strip()
        from datetime import datetime
        interval = datetime.now() - datetime.strptime(latest_page_time, "%Y/%m/%d %H:%M:%S")
        if interval.seconds < 300:  # 只采集5分钟内的更新
            target_url = "https://www.zdaye.com/" + html_tree.xpath("//h3[@class='thread_title']/a/@href")[0].strip()
            while target_url:
                _tree = WebRequest().get(target_url, verify=False).tree
                for tr in _tree.xpath("//table//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield "%s:%s" % (ip, port)
                next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
                target_url = "https://www.zdaye.com/" + next_page[0].strip() if next_page else False
                sleep(5)

    @staticmethod
    def freeSocks01():
        """
        github raw https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.json
        """
        start_url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.json"
        response = WebRequest().get(start_url).json
        for i in response:
            yield "%s:%s" % (i["ip"], i["port"])
    @staticmethod
    def freeSocks02():
        start_url = "https://sockslist.us/Api?request=display&country=all&level=all&token=free"
        response = WebRequest().get(start_url).json
        for i in response:
            yield "%s:%s" % (i["ip"], i["port"])
if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy13():
        print(_)

# http://nntime.com/proxy-list-01.htm
