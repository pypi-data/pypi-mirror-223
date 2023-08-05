import logging

logger = logging.getLogger("proxy-log")

def toBool(string) -> bool:
    match string:
        case "no":
            return False
        case "yes":
            return True
        case _:
            return False


class Proxy:
    
    proxy_counter:int = 0

    def __init__(self, proxy_data:list):
        pl = proxy_data
        self.ip = pl[0]
        self.port = int(pl[1])
        self.code = pl[2]
        self.country = pl[3]
        self.anonymous = pl[4]
        self.google_compat:bool = toBool(pl[5])
        self.https_compat:bool = toBool(pl[6])
        self.id:int = Proxy.proxy_counter
        Proxy.proxy_counter += 1

    def __repr__(self) -> str:
        return f"Proxy {self.id}: IP - {self.ip}, port - {self.port}"
    
