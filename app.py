from flask import Flask, request, jsonify
from spiders.jd_spider import crawl_jd
from spiders.dangdang_spider import crawl_dangdang
from spiders.taobao_spider import crawl_taobao

app = Flask(__name__)

@app.route("/price", methods=["GET"])
@app.route("/api/price", methods=["POST"])
def get_price():
    if request.method == "POST":
        data = request.get_json() or {}
        book = data.get("book")
    else:
        book = request.args.get("book")

    if not book:
        return jsonify({"error": "Missing 'book' parameter"}), 400

    result = {
        "jd": crawl_jd(book),
        "dangdang": crawl_dangdang(book),
        "taobao": crawl_taobao(book)
    }
    return jsonify(result)

@app.route("/")
def home():
    return "Book Price Crawler API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
