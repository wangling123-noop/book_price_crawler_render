from request_utils import request_with_proxy
from urllib.parse import quote
import json
import re

def crawl_taobao(book_name):
    url = f"https://s.taobao.com/search?q={quote(book_name)}&type=default"
    html = request_with_proxy(url)
    if not html:
        return None

    # 修正的正则表达式
    pattern = re.compile(r'g_page_config = (.*?);')
    match = pattern.search(html)
    if not match:
        return None

    data = json.loads(match.group(1))
    try:
        items = data['mods']['itemlist']['data']['auctions']
        result = []
        for item in items[:3]:
            title = re.sub("<.*?>", "", item.get("title", ""))
            price = item.get("view_price", "")
            result.append({"title": title, "price": price})
        return result
    except Exception:
        return None
