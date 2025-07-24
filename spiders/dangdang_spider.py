from request_utils import request_with_proxy
from urllib.parse import quote
from bs4 import BeautifulSoup

def crawl_dangdang(book_name):
    url = f"http://search.dangdang.com/?key={quote(book_name)}&act=input"
    html = request_with_proxy(url)
    if not html:
        print("请求当当失败，未获取到页面内容")
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".search_result_item")[:3]
        if not items:
            # 当当可能结构不一样，再尝试另一个选择器
            items = soup.select(".bigimg .name a")[:3]

        result = []
        for item in items:
            title = item.get_text(strip=True)
            parent = item.parent
            price_tag = parent.select_one(".price_n") if parent else None
            price = price_tag.get_text(strip=True) if price_tag else ""
            result.append({"title": title, "price": price})
        return result
    except Exception as e:
        print(f"解析当当页面异常: {e}")
        return None
