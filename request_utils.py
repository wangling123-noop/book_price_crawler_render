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
    },
]

def get_proxy():
    tunnel = random.choice(TUNNELS)
    proxy = f"http://{USERNAME}:{PASSWORD}@{tunnel}"
    return {"http": proxy, "https": proxy}

def request_with_proxy(url, headers=None, retries=3, timeout=10):
    for _ in range(retries):
        try:
            headers = headers or random.choice(HEADERS_LIST)
            proxies = get_proxy()
            response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                return response.text
        except Exception:
            time.sleep(random.uniform(1, 2))
    return None
