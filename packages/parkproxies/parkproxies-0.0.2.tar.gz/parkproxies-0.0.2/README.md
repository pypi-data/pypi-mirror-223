# Proxies Util

This package can be used to cycle through a list of free proxies as a way to easily obfuscate one's IP.

Create a ProxyService object like this:
`service = ProxyService(ProxyClient())`

To populate the ProxyService with a list of proxies -
`service.getProxies()`

After populating the ProxyService with proxies, filter through them by providing a dictionary of options to .filterProxies() -

```python
filters = {
    "anonymity": "anonymous",    #"anonymous" or "elite proxy"
    "code": "US",  # country code
    "google": True,  # google compatible
    "https" True,   # https compatible
}
# pass True to save filltered proxies into the ProxyService.filtered_proxies attribute
filtered_proxies = service.filterProxies(filters, True) 
```

