import urllib.request

url = "http://127.0.0.1:5000/"

print("102402116 蔡靖熹")
print("使用 urllib 访问 Flask 网站")

with urllib.request.urlopen(url, timeout=10) as response:
    print("HTTP状态码：", response.status)
    html = response.read().decode("utf-8")

print("收到的网页内容：")
print(html)