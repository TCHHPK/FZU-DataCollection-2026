from scrapy.selector import Selector

htmlText = '''
<html>
<body>
<bookstore>
<title>books</title>
<book>
<title>Novel</title>
<title lang="eng">Harry Potter</title>
<price>29.99</price>
</book>
<book>
<title>TextBook</title>
<title lang="eng">Learning XML</title>
<price>39.95</price>
</book>
</bookstore>
</body>
</html>
'''

selector = Selector(text=htmlText)

print("========== 例4-2-3 ==========")

expressions = [
    ("./title", "当前book节点的直接子节点"),
    ("/title", "从文档根节点开始的绝对路径"),
    ("//title", "全文档范围查找title")
]

for expr, description in expressions:
    s = selector.xpath("//book").xpath(expr)

    print(f"\n表达式：selector.xpath('//book').xpath('{expr}')")
    print("作用：", description)
    print("匹配数量：", len(s))

    for element in s:
        print(element)
