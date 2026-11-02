from bs4 import BeautifulSoup

html = """
<html>
<head>
    <title>BeautifulSoup测试</title>
</head>
<body>
    <h1>福州大学</h1>

    <p class="intro">数据采集课程</p>
    <p class="intro">BeautifulSoup 示例</p>
    <p id="student">102402116 蔡靖熹</p>

    <div class="course">
        <a href="https://www.fzu.edu.cn">福州大学官网</a>
        <a href="https://jwch.fzu.edu.cn">福州大学教务处</a>
    </div>

    <ul>
        <li>Python</li>
        <li>BeautifulSoup</li>
        <li>urllib</li>
    </ul>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")


# ==================================================
# 示例1：find() 查找第一个指定标签
# ==================================================
print("=" * 50)
print("示例1：find() 查找第一个 p 标签")

result = soup.find("p")

print(result)


# ==================================================
# 示例2：find_all() 查找所有指定标签
# ==================================================
print("=" * 50)
print("示例2：find_all() 查找所有 p 标签")

results = soup.find_all("p")

for item in results:
    print(item)


# ==================================================
# 示例3：find() 根据 id 属性查找
# ==================================================
print("=" * 50)
print("示例3：根据 id 属性查找")

result = soup.find("p", id="student")

print(result)


# ==================================================
# 示例4：find() 根据 class 属性查找
# ==================================================
print("=" * 50)
print("示例4：根据 class 属性查找")

result = soup.find("p", class_="intro")

print(result)


# ==================================================
# 示例5：find_all() 根据 class 查找多个元素
# ==================================================
print("=" * 50)
print("示例5：根据 class 属性查找所有元素")

results = soup.find_all("p", class_="intro")

for item in results:
    print(item)


# ==================================================
# 示例6：find_all() 使用 limit 限制返回数量
# ==================================================
print("=" * 50)
print("示例6：limit 限制返回数量")

results = soup.find_all("li", limit=2)

for item in results:
    print(item)


# ==================================================
# 示例7：通过 string 参数匹配文本
# ==================================================
print("=" * 50)
print("示例7：根据文本内容查找")

result = soup.find("p", string="BeautifulSoup 示例")

print(result)


# ==================================================
# 示例8：同时查找多个标签
# ==================================================
print("=" * 50)
print("示例8：同时查找多个标签")

results = soup.find_all(["h1", "p"])

for item in results:
    print(item)


# ==================================================
# 示例9：根据属性字典 attrs 查找
# ==================================================
print("=" * 50)
print("示例9：使用 attrs 属性查找")

result = soup.find(
    "a",
    attrs={"href": "https://www.fzu.edu.cn"}
)

print(result)


# ==================================================
# 示例10：获取标签中的文本和属性
# ==================================================
print("=" * 50)
print("示例10：获取标签文本和属性")

result = soup.find("a")

print("完整标签：", result)
print("标签文本：", result.get_text())
print("href属性：", result.get("href"))