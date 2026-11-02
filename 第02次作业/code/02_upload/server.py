from pathlib import Path
from flask import Flask, request

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload():
    file_name = request.args.get("fileName", "")

    if not file_name or Path(file_name).name != file_name:
        return "文件名称无效", 400

    data = request.get_data()
    save_path = UPLOAD_DIR / ("upload_" + file_name)
    save_path.write_bytes(data)

    print(f"收到文件：{file_name}，共{len(data)}字节", flush=True)
    print(f"保存位置：{save_path}", flush=True)
    return "OK"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
