import os
import dotenv
from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from gh_md_to_html.core_converter import markdown

from .merger import Merger

# load environment variables from .env file, if defined
dotenv.load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])


@app.route("/", methods=["GET"])
def index():
    with open("README.md", "r") as f:
        readme_md = f.read()
    readme_html = markdown(readme_md)
    return render_template("index.html", content=readme_html)


@app.route("/api/v1.0/", methods=["OPTIONS", "POST"])
def merge():
    if request.method == "OPTIONS":
        return make_response(jsonify({"Allow": "POST"}), 200)

    foreground_url = request.json.get("foreground_url")
    background_url = request.json.get("background_url")

    if not foreground_url or not background_url:
        abort(400)

    try:
        m = Merger(foreground_url, background_url)
        m.merge_images()
        response = {
            "output_image": {
                "name": m.get_output_image("name"),
                "url": url_for(
                    "get_image", image_name=m.get_output_image("name"), _external=True
                ),
                "base64": m.get_output_image("base64"),
            }
        }
        return jsonify(response), 201
    except Exception as e:
        err_msg = getattr(e, "message", None)
        if not err_msg:
            err_msg = "Internal Error. Please Try Again"
        return make_response(jsonify({"error": err_msg}), 500)


@app.route("/image/<string:image_name>", methods=["GET"])
def get_image(image_name):
    return send_from_directory(app.config["OUTPUT_IMAGES_FOLDER"], image_name)


@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({"error": "Internal Server Error"}), 500)


@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({"error": "Method Not Allowed"}), 405)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad Request"}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)
