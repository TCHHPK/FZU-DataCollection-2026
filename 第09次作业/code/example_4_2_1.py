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

print("========== 例4-2-1 ==========")
print("Selector类型：", type(selector))
print("Selector对象：", selector)

s = selector.xpath("//title")

print("查询表达式：//title")
print("查询结果类型：", type(s))
print("查询结果：", s)
print("找到的title数量：", len(s))
