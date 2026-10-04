# 作业1
# 102402116蔡靖熹 
import flask

app = flask.Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        # 获取 URL 中的 GET 参数
        province = flask.request.args.get("province", "")
        city = flask.request.args.get("city", "")

        # 获取 POST 表单参数
        post_province = flask.request.form.get("province", "")
        post_city = flask.request.form.get("city", "")
        note = flask.request.form.get("note", "")

        # 如果 province/city 是 POST 传来的，就使用 POST 数据
        if post_province:
            province = post_province

        if post_city:
            city = post_city

        # 返回结果
        result = province + "," + city

        if note:
            result += "\n" + note

        return result

    except Exception as err:
        return str(err)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )