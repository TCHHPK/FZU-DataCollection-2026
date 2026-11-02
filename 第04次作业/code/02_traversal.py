from bs4 import BeautifulSoup

html = """
<html>
<head>
    <title>BeautifulSoup遍历测试</title>
</head>
<body>
    <div id="content">
        <h1>福州大学</h1>
        <p>数据采集课程</p>
        <ul>
            <li>Python</li>
            <li>BeautifulSoup</li>
            <li>urllib</li>
        </ul>
    </div>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")


# ==================================================
# 一、向下遍历
# ==================================================
print("=" * 50)
print("一、向下遍历")

div = soup.find("div", id="content")

print("\n1. contents：获取直接子节点")
print(div.contents)

print("\n2. children：遍历直接子节点")
for child in div.children:
    print(child)

print("\n3. descendants：遍历所有后代节点")
for descendant in div.descendants:
    print(descendant)


# ==================================================
# 二、向上遍历
# ==================================================
print("=" * 50)
print("二、向上遍历")

li = soup.find("li")

print("\n1. parent：获取父节点")
print(li.parent)

print("\n2. parents：遍历所有祖先节点")
for parent in li.parents:
    print(parent.name)


# ==================================================
# 三、平行遍历
# ==================================================
print("=" * 50)
print("三、平行遍历")

p = soup.find("p")

print("\n1. next_sibling：获取下一个兄弟节点")
print(p.next_sibling)

print("\n2. previous_sibling：获取上一个兄弟节点")
print(p.previous_sibling)

print("\n3. next_siblings：遍历后面的兄弟节点")
for sibling in p.next_siblings:
    print(sibling)

print("\n4. previous_siblings：遍历前面的兄弟节点")
for sibling in p.previous_siblings:
    print(sibling)