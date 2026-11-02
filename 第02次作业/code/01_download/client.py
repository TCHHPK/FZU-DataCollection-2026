from pathlib import Path
import urllib.parse
import urllib.request

BASE_DIR = Path(__file__).resolve().parent
url = "http://127.0.0.1:5000/"

print("102402116 蔡靖熹")
print("实践案例：Web下载文件")

# 第一次请求：获取文件名称
with urllib.request.urlopen(url, timeout=10) as response:
    file_name = response.read().decode("utf-8")

print("准备下载：", file_name)

# 第二次请求：下载文件数据
query = urllib.parse.urlencode({"fileName": file_name})

with urllib.request.urlopen(url + "?" + query, timeout=10) as response:
    print("HTTP状态码：", response.status)
    data = response.read()

save_path = BASE_DIR / ("download_" + Path(file_name).name)
save_path.write_bytes(data)

print("下载完毕：", len(data), "字节")
print("保存位置：", save_path)
print("下载文件内容：")
print(save_path.read_text(encoding="utf-8"))

# 本地实验中，比较服务器源文件与下载文件
source_path = BASE_DIR / file_name
print("文件内容一致：", source_path.read_bytes() == data)