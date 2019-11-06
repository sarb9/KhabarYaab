from flask import Flask, render_template, request, jsonify

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['JSON_AS_ASCII'] = False

output_search_res = [
    {"title": "milad", "description": ",سپاه پاسداران جمهوری اسلامی ایران سپاه پاسداران جمهوری اسلامی ایران ",
     "img": "http://google.com"},
    {"title": "arad", "description": "خرمشهرررررر آزاد شددددددد ",
     "img": "http://google.me"},
    {"title": "alireza", "description": "قیمت دلااررر کاهش یافتتتتتتتت ",
     "img": "http://google.you"},
    {"title": "mehdi", "description": ",دستگیری دو عامل دزدی در بازار تهران ",
     "img": "http://google.him"}
]

output_news_content = {"title": "پیروزی انقلاب یمن",
                       "description": ",سپاه پاسداران جمهوری اسلامی ایران سپاه پاسداران جمهوری اسلامی ایران ",
                       "img": "http://google.com",
                       "content": "میووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییمیووویصصشیشصیشصییوووووووو"},


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/search", methods=['GET'])
def search():
    # todo: search query method in BTree must be called here and results !
    if request.args.get("q"):
        results = output_search_res
        print("soorie")
        return jsonify({"news_headers": results})


@app.route("/news/<int:news_id>", methods=['GET'])
def get_news(news_id):
    results = output_news_content
    return jsonify(results)


if __name__ == "__main__":
    app.run()
