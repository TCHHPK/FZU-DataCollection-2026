from pathlib import Path
import urllib.parse
import urllib.request

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "待上传文件.txt"
url = "http://127.0.0.1:5000/upload"

print("102402116 蔡靖熹")
print("实践案例：Web上传文件")

data = file_path.read_bytes()
query = urllib.parse.urlencode({"fileName": file_path.name})

req = urllib.request.Request(
    url + "?" + query,
    data=data,
    headers={"Content-Type": "application/octet-stream"},
    method="POST",
)

print("准备上传：", file_path.name)
print("请求方式：", req.get_method())

with urllib.request.urlopen(req, timeout=10) as response:
    print("HTTP状态码：", response.status)
    message = response.read().decode("utf-8")

print("服务器返回：", message)

if message == "OK":
    print("成功上传：", len(data), "字节")

    # 本地实验：检查服务器保存的文件
    saved_path = BASE_DIR / "uploads" / ("upload_" + file_path.name)
    print("服务器文件位置：", saved_path)
    print("文件内容一致：", saved_path.read_bytes() == data)
    print("服务器保存的内容：")
    print(saved_path.read_text(encoding="utf-8"))
