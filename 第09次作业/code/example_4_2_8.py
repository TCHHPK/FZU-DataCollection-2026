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

print("========== 例4-2-8 ==========")

s = selector.xpath("//book/title[@lang='chinese']/text()")
print("\n1. 根据 lang 属性筛选：")
print("XPath：//book/title[@lang='chinese']/text()")
print("结果：", s.extract_first())

s = selector.xpath("//book[@id='b1']/title")
print("\n2. 根据 id 属性筛选：")
print("XPath：//book[@id='b1']/title")
print("结果：", s.extract_first())
