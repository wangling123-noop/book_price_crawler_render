from bs4 import BeautifulSoup
from urllib.parse import quote
from request_utils import request_with_proxy

def crawl_dangdang(book_name):
    url = f"http://search.dangdang.com/?key={quote(book_name)}&act=input"
    html = request_with_proxy(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("ul.bigimg li")
    result = []

    for item in items[:3]:
        title_tag = item.select_one("a[name='itemlist-title']")
        price_tag = item.select_one("p.price span.search_now_price")
        if title_tag and price_tag:
            title = title_tag.get("title")
            price = price_tag.get_text(strip=True)
            result.append({"title": title, "price": price})

    return result
