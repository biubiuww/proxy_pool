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
    
    @staticmethod
    def freeSocks03():
        start_url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=socks4&proxy_format=protocolipport&format=text&timeout=20000"
        response = WebRequest().get(start_url).text
        proxy = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", response)
        for _ in proxy:
            yield _

    @staticmethod
    def freeSocks04():
        start_urls = ["https://www.freeproxy.world/?type=socks5&anonymity=&country=&speed=&port=&page={}".format(i) for i in range(1, 4)]
        for url in start_urls:
            response = WebRequest().get(url).text
            ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response)
            port = re.findall(r"\d{1,5}</a>", response)
            for i in zip(ip, port):
                ip = i[0]
                port = i[1].replace("</a>", "")
                yield "{}:{}".format(ip, port)
    @staticmethod
    def freeLocalhost():
        """
        读取本地json文件，每次只返回一个代理
        """
        data = []
        with open("test_req.json",'r',encoding='utf-8') as f:
            for line in f:
                try:
                    data.append(json.loads(line.rstrip('\n')))
                except:
                    pass
        for _ in data:
            yield "{}".format(_.get("host"))
    @staticmethod
    def freeSocks05():
        start_url = "https://freeproxyupdate.com/socks5-proxy"
        response = WebRequest().get(start_url).tree
        table = response.xpath('//*[@id="main-content"]/table')
        try:
            for tr in table[0].xpath('./tbody/tr'):
                ip = tr.xpath('./td[1]/text()')[0]
                port = tr.xpath('./td[2]/text()')[0]
                yield "{}:{}".format(ip, port)
        except Exception as e:
            pass
    
    @staticmethod
    def freeSocks06():
        start_url = "https://www.proxysharp.com/proxies/socks5"
        response = WebRequest().get(start_url).tree
        table = response.xpath('//*[@id="proxies-full"]/tbody')
        for tr in table[0].xpath('./tr'):
            try:
                host = tr.xpath('./td[1]/text()')[0]
                yield f"{host}"
            except Exception as e:
                pass
    @staticmethod
    def freeSocks07():
        start_url = "https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500&page=1&sort_by=lastChecked&sort_type=desc"
        response = WebRequest().get(start_url).json
        for _ in response["data"]:
            yield f"{_['ip']}:{_['port']}"

if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy13():
        print(_)

# http://nntime.com/proxy-list-01.htm
