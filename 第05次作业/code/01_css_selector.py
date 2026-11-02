from bs4 import BeautifulSoup

html = """
<html>
<head>
    <title>CSS选择器测试</title>
</head>
<body>
    <div id="main">
        <h1 class="title">福州大学</h1>

        <p class="course">数据采集课程</p>
        <p class="course important">BeautifulSoup CSS选择器</p>

        <ul class="list">
            <li>Python</li>
            <li>BeautifulSoup</li>
            <li>urllib3</li>
        </ul>

        <div class="links">
            <a href="https://www.fzu.edu.cn">福州大学官网</a>
            <a href="https://jwch.fzu.edu.cn">福州大学教务处</a>
        </div>

        <p id="student">102402116 蔡靖熹</p>
    </div>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")


# ==================================================
# 实例2-5-1：使用标签名选择元素
# ==================================================
print("=" * 50)
print("实例2-5-1：标签选择器")

results = soup.select("p")

for item in results:
    print(item)


# ==================================================
# 实例2-5-2：使用 class 选择元素
# ==================================================
print("=" * 50)
print("实例2-5-2：class 选择器")

results = soup.select(".course")

for item in results:
    print(item)


# ==================================================
# 实例2-5-3：使用 id 选择元素
# ==================================================
print("=" * 50)
print("实例2-5-3：id 选择器")

results = soup.select("#student")

for item in results:
    print(item)


# ==================================================
# 实例2-5-4：使用层级选择器
# ==================================================
print("=" * 50)
print("实例2-5-4：层级选择器")

results = soup.select("div.links a")

for item in results:
    print(item)


# ==================================================
# 实例2-5-5：使用属性选择器
# ==================================================
print("=" * 50)
print("实例2-5-5：属性选择器")

results = soup.select('a[href="https://www.fzu.edu.cn"]')

for item in results:
    print(item)