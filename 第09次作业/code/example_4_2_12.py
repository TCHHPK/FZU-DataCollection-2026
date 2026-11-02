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

print("========== 例4-2-12 ==========")

s = selector.xpath(
    "//title[@lang='chinese']/parent::*"
)

print("\nXPath：//title[@lang='chinese']/parent::*")
print("匹配数量：", len(s))
print("父节点内容：")

for element in s.extract():
    print(element)

print("\n父节点id属性：", s.xpath("./@id").getall())
