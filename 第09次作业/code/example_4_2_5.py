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

print("========== 例4-2-5 ==========")

s = selector.xpath("//book/@id")

print("\n1. XPath 查询结果：")
print(s)

print("\n2. extract() 提取属性值：")
print(s.extract())

print("\n3. 遍历每个属性节点：")
for e in s:
    print(e.extract())
