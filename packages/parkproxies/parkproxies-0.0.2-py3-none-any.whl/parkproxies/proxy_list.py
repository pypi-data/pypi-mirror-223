from proxy import Proxy
import logging
import requests
import bs4 as bs
import time


logger = logging.getLogger("proxy-log")

def getTime() -> str:
    return time.asctime(time.localtime())

class ProxyClient:
    """Provides access to a list of free proxies, and utilities for working with them."""
    proxies_url = "https://free-proxy-list.net/"
    def __init__(self):
        self.key = {}
        self.proxies_list:list[Proxy] = []
        self.filtered_proxies = []
    
    def getProxies(self) -> list[Proxy]:
        proxies = []
        response = requests.get("https://free-proxy-list.net/")
        if response.status_code != 200:
            logger.error(f"HTTP response to {ProxyClient.proxies_url} returned a bad status code.")
            return []
        soup = bs.BeautifulSoup(response.content, features="html.parser")
        table = soup.find(name='table', attrs={"class":"table table-striped table-bordered"})
        if table == None:
            logger.error(f"Failed to retrieve Proxies table from {ProxyClient.proxies_url}")
            return []
        table_head = table.thead.tr
        head_elements = table_head.findChildren()
        count = 0
        for child in head_elements:
            self.key[child.contents[0].lower()] = count
            count += 1
        # print(self.key)
        table_contents = table.tbody
        rows = table_contents.findChildren()
        for row in rows:
            cols = row.find_all('td')
            logger.debug(cols)
            proxy_data = [ele.text.strip() for ele in cols]
            if len(proxy_data) >= 7:
                proxy = Proxy(proxy_data)
                proxies.append(proxy)
        self.proxies_list = proxies
        return proxies
    
    def filter_proxies(self, describers:dict) -> list[Proxy]:
        filters = {}
        # do some little validation of proxies
        for attribute in describers:
            if attribute in self.key:
                filters[attribute] = describers[attribute]
        # make sure all the provided pairs are valid
        filtered_proxies = self.proxies_list.copy()
        for filter in filters:
            match filter:
                case "anonymous":
                    filtered_proxies = [proxy for proxy in filtered_proxies if proxy.anonymous == describers[filter]]
                case "code":
                    filtered_proxies = [proxy for proxy in filtered_proxies if proxy.code == describers[filter]]
                case "google":  
                    filtered_proxies = [proxy for proxy in filtered_proxies if proxy.google_compat == describers[filter]]
                case "https":
                    filtered_proxies = [proxy for proxy in filtered_proxies if proxy.https_compat == describers[filter]]
                case _:
                    print(f"This filter {filter} is not valid.")
        return filtered_proxies
    
    
    def __getitem__(self, key) -> Proxy | None:
        try:
            return self.proxies_list[key]
        except IndexError as e:
            logger.error(f"{getTime()}: Index error while trying to access item of ProxyList. Make sure you getProxies() before trying to access elements.")
            return None

