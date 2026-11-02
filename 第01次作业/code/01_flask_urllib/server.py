from pathlib import Path
from flask import Flask

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent


@app.route("/")
def index():
    return (BASE_DIR / "index.html").read_text(encoding="utf-8")


@app.route("/hi")
def hi():
    return "Hi，你好！102402116 蔡靖熹"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)