from flask import Flask, render_template, request, jsonify

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['JSON_AS_ASCII'] = False

app = None


class FlaskServer:
    search_method = None
    get_content_method = None

    # get_similars = None

    def __init__(self, search_method, get_content_method, get_similars):
        global app
        # app.DEBUG = True
        app = Flask(__name__)
        app.config.from_object(__name__)
        app.config['JSON_AS_ASCII'] = False
        self.search_method = search_method
        self.get_content_method = get_content_method
        self.get_similars = get_similars

        @app.route("/")
        def main():
            return render_template("index.html")

        @app.route("/search", methods=['GET'])
        def search():
            # todo: search query method in BTree must be called here and results !
            if request.args.get("q"):
                results = search_method(request.args.get("q"))
                # print("$$$$$$$$$$$   RRREEEEESSSSS      $$$$$$$$$  ", len(results), "\n", results)
                return jsonify({"news_headers": results})

        @app.route("/news/<int:news_id>", methods=['GET'])
        def get_news(news_id):
            # results = output_news_content
            results = get_content_method(news_id)
            return jsonify(results)

        @app.route("/similar/<int:news_id>", methods=['GET'])
        def similars(news_id):
            res = get_similars(news_id)
            return jsonify(res)

    def run(self):
        global app
        app.run(threaded=False, processes=1)
