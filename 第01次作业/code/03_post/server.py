from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    province = request.form.get("province", "")
    city = request.form.get("city", "")

    return f"收到POST参数：{province},{city}"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)