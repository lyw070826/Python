import re
import time
import random
import requests
import threading

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}
proxy = {}
proxy_ok = {}
def get_proxy_server(url):
    global proxy
    requ = requests.get(url,headers=headers)
    urls = re.findall(r'<td data-title="IP">(.*?)</td>',requ.text)
    ports = re.findall(r'<td data-title="PORT">(.*?)</td>',requ.text)
    for x in range(len(urls)) :
        proxy[urls[x]] = ports[x]
    return proxy
def test_proxy_ip():
    global proxy,proxy_ok
    for x in list(proxy):
        proxy_test = {"https" : "{0}:{1}".format(x,proxy[x])}
        try :
            requ = requests.get("https://www.baidu.com/",headers=headers,proxies=proxy_test,timeout=3)
            status = requ.status_code
            if status == 200 :
                proxy_ok[x] = proxy[x]
        except Exception as identifier:
            print(identifier)
            continue
    return proxy_ok
def start_get_proxy_ip(times):
    # times = input("页数:  ")
    for x in range(int(times)):
        print('https://www.kuaidaili.com/free/inha/{0}/'.format(str(x+1)))
        get_proxy_server('https://www.kuaidaili.com/free/inha/{0}/'.format(str(x+1)))
        time.sleep(random.randint(4,8))
    test_proxy_ip()

start_get_proxy_ip(1)
