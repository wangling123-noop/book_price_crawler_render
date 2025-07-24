import requests
import random
import time

USERNAME = "t15332794831619"
PASSWORD = "78wssuy2"
TUNNELS = [
    "p385.kdltps.com:15818",
    "p386.kdltps.com:15818",
]

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
        "Connection": "close"
    },
    # 可以添加更多User-Agent，模拟多样化浏览器
]

def get_proxy():
    tunnel = random.choice(TUNNELS)
    proxy_url = f"http://{USERNAME}:{PASSWORD}@{tunnel}"
    return {
        "http": proxy_url,
        "https": proxy_url,
    }

def request_with_proxy(url, headers=None, retries=3, timeout=10):
    """
    使用快代理隧道IP发起请求，带重试，自动切换代理
    :param url: 请求目标URL
    :param headers: 可选HTTP头
    :param retries: 重试次数
    :param timeout: 超时秒数
    :return: 响应内容字符串或None
    """
    for attempt in range(retries):
        try:
            _headers = headers or random.choice(HEADERS_LIST)
            proxies = get_proxy()
            response = requests.get(url, headers=_headers, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                return response.text
            else:
                print(f"请求失败，状态码：{response.status_code}")
        except Exception as e:
            print(f"请求异常：{e}，正在重试 {attempt+1}/{retries} ...")
            time.sleep(random.uniform(1, 2))
    return None
