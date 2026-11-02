from scrapy.selector import Selector

htmlText = '''
<html><body>
<bookstore>
<book>
<title lang="eng">Harry Potter</title>
<price>29.99</price>
</book>
<book>
<title lang="eng">Learning XML</title>
<price>39.95</price>
</book>
</bookstore>
</body></html>
'''

selector = Selector(text=htmlText)

expressions = [
    "//bookstore/book",
    "//body/book",
    "//body//book",
    "/body//book",
    "/html/body//book",
    "/html//book",
    "//book/title",
    "//title",
    "//bookstore//title",
    "//book//price",
    "//price"
]

print("========== 例4-2-2 ==========")

for expr in expressions:
    result = selector.xpath(expr)
    print(f"{expr:<25} 匹配数量：{len(result)}")
    print("提取结果：", result.extract())
    print("-" * 55)
