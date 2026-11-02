import urllib.parse
import urllib.request

url = "http://127.0.0.1:5000/"
params = {
    "province": "广东",
    "city": "深圳",
}

query = urllib.parse.urlencode(params)
request_url = url + "?" + query

print("102402116 蔡靖熹")
print("请求方式：GET")
print("请求地址：", request_url)

with urllib.request.urlopen(request_url, timeout=10) as response:
    print("HTTP状态码：", response.status)
    print("服务器返回：", response.read().decode("utf-8"))
    