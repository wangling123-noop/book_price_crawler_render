from bs4 import BeautifulSoup
from urllib.parse import quote
from request_utils import request_with_proxy

def crawl_jd(book_name):
    url = f"https://search.jd.com/Search?keyword={quote(book_name)}&enc=utf-8"
    html = request_with_proxy(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".gl-item")
    result = []

    for item in items[:3]:
        name_tag = item.select_one(".p-name em")
        price_tag = item.select_one(".p-price i")
        if name_tag and price_tag:
            name = name_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            result.append({"title": name, "price": price})

    return result
