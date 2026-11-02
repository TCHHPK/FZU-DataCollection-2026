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

print("========== 例4-2-9 ==========")

s = selector.xpath("//book[position()=1]/title")
print("\n1. 第一本书：")
print("XPath：//book[position()=1]/title")
print("结果：", s.extract_first())

s = selector.xpath("//book[position()=2]/title")
print("\n2. 第二本书：")
print("XPath：//book[position()=2]/title")
print("结果：", s.extract_first())
