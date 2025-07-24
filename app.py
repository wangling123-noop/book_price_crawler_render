from flask import Flask, request, jsonify
from spiders.jd_spider import crawl_jd
from spiders.dangdang_spider import crawl_dangdang
from spiders.taobao_spider import crawl_taobao

app = Flask(__name__)

@app.route("/api/price", methods=["POST"])
def get_price():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    # 支持传入数组或者单个对象
    if isinstance(data, list):
        books = []
        for item in data:
            if isinstance(item, dict) and "book" in item:
                books.append(item["book"])
        if not books:
            return jsonify({"error": "No valid 'book' field found in array"}), 400
    elif isinstance(data, dict):
        book = data.get("book")
        if not book:
            return jsonify({"error": "Missing 'book' field"}), 400
        books = [book]
    else:
        return jsonify({"error": "Invalid JSON format"}), 400

    results = []
    for b in books:
        result = {
            "book": b,
            "jd": crawl_jd(b),
            "dangdang": crawl_dangdang(b),
            "taobao": crawl_taobao(b)
        }
        results.append(result)

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
