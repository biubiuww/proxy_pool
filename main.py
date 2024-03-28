from flask import Flask
from handler.proxyHandler import ProxyHandler
from handler.configHandler import ConfigHandler
from api.proxyApi import runFlask

app = Flask(__name__)
conf = ConfigHandler()
proxy_handler = ProxyHandler()

if __name__=="__main__":
    runFlask()