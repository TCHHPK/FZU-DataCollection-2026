# 作业1
# 102402116蔡靖熹 

import urllib.parse
import urllib.request


url = "http://127.0.0.1:5000"

# 作业1
# 102402116蔡靖熹 
# --------------------------------------------------
# 1. POST 请求
# province 和 city 放在 POST 表单中
# --------------------------------------------------

def test_post():
    try:
        province = urllib.parse.quote("广东")
        city = urllib.parse.quote("深圳")

        data = "province=" + province + "&city=" + city

        # urlopen 的 data 参数需要二进制数据
        data = data.encode()

        response = urllib.request.urlopen(
            url,
            data=data
        )

        html = response.read()
        html = html.decode()

        print("POST 请求结果：")
        print(html)

    except Exception as err:
        print(err)

# 作业1
# 102402116蔡靖熹 
# --------------------------------------------------
# 2. GET 请求
# province 和 city 放在 URL 中
# --------------------------------------------------

def test_get():
    try:
        province = urllib.parse.quote("广东")
        city = urllib.parse.quote("深圳")

        data = "province=" + province + "&city=" + city

        response = urllib.request.urlopen(
            url + "?" + data
        )

        html = response.read()
        html = html.decode()

        print("GET 请求结果：")
        print(html)

    except Exception as err:
        print(err)

# 作业1
# 102402116蔡靖熹 
# --------------------------------------------------
# 3. GET + POST 混合请求
#
# province、city 使用 GET
# note 使用 POST
# --------------------------------------------------

def test_get_post():
    note = (
        "深圳依山傍海，气候宜人，实在是适合人类居住的绝佳地。"
        "这里四季如春，干净整洁，比邻香港，拥有着丰富的自然景观和人文气息。"
        "匆匆过客注意到的也许只有它的时尚繁华，"
        "忙碌的暂居者也可能对它有着不识城市真面目之感。"
        "只有世代在此生活的老深圳人，"
        "才默默的看着它从贫穷走向富饶经历了怎样的艰辛。"
    )

    try:
        province = urllib.parse.quote("广东")
        city = urllib.parse.quote("深圳")

        # GET 参数
        param = "province=" + province + "&city=" + city

        # POST 参数
        note_data = "note=" + urllib.parse.quote(note)

        response = urllib.request.urlopen(
            url + "?" + param,
            data=note_data.encode()
        )

        html = response.read()
        html = html.decode()

        print("GET + POST 请求结果：")
        print(html)

    except Exception as err:
        print(err)

# 作业1
# 102402116蔡靖熹 
# --------------------------------------------------
# 4. 最普通的 GET 请求
# --------------------------------------------------

def test_simple_get():
    try:
        response = urllib.request.urlopen(url)

        data = response.read()
        html = data.decode()

        print("普通 GET 请求结果：")
        print(html)

    except Exception as err:
        print(err)


# --------------------------------------------------
# 程序入口
# --------------------------------------------------

if __name__ == "__main__":

    print("===== 测试 GET =====")
    test_get()

    print()

    print("===== 测试 POST =====")
    test_post()

    print()

    print("===== 测试 GET + POST =====")
    test_get_post()

    print()

    print("===== 测试普通 GET =====")
    test_simple_get()