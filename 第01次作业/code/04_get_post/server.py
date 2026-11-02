from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    province = request.args.get("province", "")
    city = request.args.get("city", "")
    note = request.form.get("note", "")

    return (
        f"请求方式：{request.method}\n"
        f"URL查询参数：{province},{city}\n"
        f"POST表单参数：{note}"
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)