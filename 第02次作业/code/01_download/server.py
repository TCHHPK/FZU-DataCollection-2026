from pathlib import Path
from flask import Flask, request, send_file

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = "示例文件.txt"


@app.route("/", methods=["GET"])
def download():
    file_name = request.args.get("fileName")

    # 第一次访问：返回可下载的文件名称
    if file_name is None:
        return FILE_NAME

    # 第二次访问：返回指定文件的二进制数据
    if file_name != FILE_NAME:
        return "文件不存在", 404

    return send_file(
        BASE_DIR / FILE_NAME,
        as_attachment=True,
        download_name=FILE_NAME,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
    