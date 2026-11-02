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

print("========== 例4-2-10 ==========")

s = selector.xpath("//bookstore/*/title")

print("XPath：//bookstore/*/title")
print("匹配数量：", len(s))
print("提取结果：")

for element in s.extract():
    print(element)
