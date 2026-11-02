from scrapy.selector import Selector

# ====================================
# 例 4-2-7-1：多个直接文本节点
# ====================================

htmlText1 = '''
<html>
<body>
<bookstore>
<book id="b1">
<title lang="english"><b>H</b>arry <b>P</b>otter</title>
<price>29.99</price>
</book>
</bookstore>
</body>
</html>
'''

selector1 = Selector(text=htmlText1, type="xml")

print("========== 例4-2-7-1 ==========")

s = selector1.xpath("//book/title/text()")

print("XPath：//book/title/text()")
print("b 子元素数量：", len(selector1.xpath("//book/title/b")))
print("查询结果：", s)
print("extract()：", s.extract())

print("逐个输出：")
for e in s:
    print(repr(e.extract()))


# ====================================
# 例 4-2-7-2：访问子节点文本
# ====================================

htmlText2 = '''
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
<title lang="eng">Learning <b>XML</b></title>
<price>39.95</price>
</book>
</bookstore>
</body>
</html>
'''

selector2 = Selector(text=htmlText2, type="xml")

print("\n========== 例4-2-7-2 ==========")

print("b 子元素数量：", len(selector2.xpath("//book/title/b")))

s1 = selector2.xpath("//book").xpath("./title//text()")
print("\nXPath：//book → ./title//text()")
print("包含子孙节点的文本：", s1.extract())

s2 = selector2.xpath("//book").xpath("./title/text()")
print("\nXPath：//book → ./title/text()")
print("仅直接文本节点：", s2.extract())

# ====================================
# 自动验证实验结果
# ====================================

assert selector1.xpath("//book/title/text()").getall() == [
    "arry ", "otter"
], "4-2-7-1 结果不符合预期"

assert s1.getall() == [
    "Novel", "Harry Potter", "TextBook", "Learning ", "XML"
], "4-2-7-2 后代文本结果不符合预期"

assert s2.getall() == [
    "Novel", "Harry Potter", "TextBook", "Learning "
], "4-2-7-2 直接文本结果不符合预期"

print("\n========== 验证完成：全部通过 ==========")
