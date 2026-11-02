from scrapy.selector import Selector

htmlText = '''
<html>
<body>
<bookstore>
<book>
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

print("========== 例4-2-11 ==========")

s = selector.xpath("//book[@*]/title")
print("\n1. 查找具有任意属性的book元素：")
print("XPath：//book[@*]/title")
print("匹配数量：", len(s))
print("结果：", s.extract())

s = selector.xpath("//@*")
print("\n2. 提取文档中全部属性值：")
print("XPath：//@*")
print("结果：", s.extract())
