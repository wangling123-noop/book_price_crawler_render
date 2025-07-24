from request_utils import request_with_proxy
from urllib.parse import quote
import json
import re

def crawl_taobao(book_name):
    url = f"https://s.taobao.com/search?q={quote(book_name)}&type=default"
    html = request_with_proxy(url)
    if not html:
        print("请求淘宝失败，未获取到页面内容")
        return None

    # 正则提取 g_page_config 对应的 JSON 字符串
    pattern = re.compile(r'g_page_config\s*=\s*(\{.*?\});')
    match = pattern.search(html)
    if not match:
        print("淘宝页面未找到 g_page_config 数据")
        return None

    try:
        data_json = match.group(1)
        data = json.loads(data_json)
    except Exception as e:
        print(f"解析淘宝 JSON 数据失败: {e}")
        return None

    try:
        items = data['mods']['itemlist']['data']['auctions']
        result = []
        for item in items[:3]:
            title = re.sub("<.*?>", "", item.get("title", ""))
            price = item.get("view_price", "")
            result.append({"title": title, "price": price})
        return result
    except Exception as e:
        print(f"提取淘宝商品数据异常: {e}")
        return None
