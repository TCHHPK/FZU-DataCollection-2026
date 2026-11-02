from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    province = request.args.get("province", "")
    city = request.args.get("city", "")

    return f"收到GET参数：{province},{city}"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)