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

app = None

class FlaskServer:
    search_method = None
    get_content_method = None

    def __init__(self, search_method, get_content_method):
        global app
        EBUG = True
        app = Flask(__name__)
        app.config.from_object(__name__)
        app.config['JSON_AS_ASCII'] = False
        self.search_method = search_method
        self.get_content_method = get_content_method

        @app.route("/")
        def main():
            return render_template("index.html")

        @app.route("/search", methods=['GET'])
        def search():
            # todo: search query method in BTree must be called here and results !
            if request.args.get("q"):
                results = search_method(request.args.get("q"))
                return jsonify({"news_headers": results})

        @app.route("/news/<int:news_id>", methods=['GET'])
        def get_news(news_id):
            # results = output_news_content
            results = get_content_method(news_id)
            return jsonify(results)

    def run(self):
        global app
        app.run()
