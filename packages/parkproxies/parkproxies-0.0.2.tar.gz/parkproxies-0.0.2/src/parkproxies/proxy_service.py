
from proxy_list import ProxyClient
from proxy import Proxy
import logging
import time

def getTime() -> str:
    return time.asctime(time.localtime())

logger = logging.Logger("proxy-log")
handler = logging.FileHandler("proxy.log", mode="w", encoding="utf-8")
logger.addHandler(handler)


class ProxyService:
    def __init__(self, proxy_client:ProxyClient):
        self.client = proxy_client
        self.proxies = []
        self.current_proxy = None
        self.filtered_proxies = []
    
    def addProxies(self, new_proxies:list):
        for proxy in new_proxies:
            self.proxies.append(proxy)
        
    def getProxies(self) -> list[Proxy]:
        new_proxies = self.client.getProxies()
        return new_proxies

    def filterProxies(self, filters:dict, addToSelf:bool) -> list[Proxy]:
        filtered_proxies = self.client.filter_proxies(filters)
        if addToSelf:
            self.filtered_proxies += filtered_proxies
        return filtered_proxies

