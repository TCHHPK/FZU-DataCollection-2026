import urllib.parse
import urllib.request

url = "http://127.0.0.1:5000/"

query = urllib.parse.urlencode({
    "province": "广东",
    "city": "深圳",
})

data = urllib.parse.urlencode({
    "note": "深圳依山傍海，气候宜人，拥有丰富的自然景观和人文气息。",
}).encode("utf-8")

req = urllib.request.Request(
    url + "?" + query,
    data=data,
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    },
    method="POST",
)

print("102402116 蔡靖熹")
print("实践案例：GET+POST混合传参")
print("请求方式：", req.get_method())
print("请求地址：", req.full_url)
print("请求正文：", data.decode("utf-8"))

with urllib.request.urlopen(req, timeout=10) as response:
    print("HTTP状态码：", response.status)
    print("服务器返回：")
    print(response.read().decode("utf-8"))