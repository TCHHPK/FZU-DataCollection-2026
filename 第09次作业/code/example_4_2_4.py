from scrapy.selector import Selector

htmlText = '''
<html>
<body>
<bookstore>
<book id="b1">
<title lang="english">Harry Potter</title>
<price>29.99</price>
</book>
<book id="b2">
<title lang="chinese">学习XML</title>
<price>39.95</price>
</book>
</bookstore>
</body></html>
'''

selector = Selector(text=htmlText)

print("========== 例4-2-4 ==========")

s = selector.xpath("//book/price")
print("\n1. 原始 XPath 查询结果")
print("类型：", type(s))
print("结果：", s)

s = selector.xpath("//book/price").extract()
print("\n2. extract() 提取结果")
print("类型：", type(s))
print("结果：", s)

s = selector.xpath("//book/price").extract_first()
print("\n3. extract_first() 提取结果")
print("类型：", type(s))
print("结果：", s)
