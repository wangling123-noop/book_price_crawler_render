from request_utils import request_with_proxy
from urllib.parse import quote
from bs4 import BeautifulSoup

def crawl_jd(book_name):
    url = f"https://search.jd.com/Search?keyword={quote(book_name)}"
    html = request_with_proxy(url)
    if not html:
        print("请求京东失败，未获取到页面内容")
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("#J_goodsList .gl-item")[:3]
        result = []
        for item in items:
            title_tag = item.select_one(".p-name em")
            price_tag = item.select_one(".p-price strong i")
            title = title_tag.get_text(strip=True) if title_tag else ""
            price = price_tag.get_text(strip=True) if price_tag else ""
            result.append({"title": title, "price": price})
        return result
    except Exception as e:
        print(f"解析京东页面异常: {e}")
        return None
