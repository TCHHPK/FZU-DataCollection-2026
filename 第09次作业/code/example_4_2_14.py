from scrapy.selector import Selector

htmlText = '''
<a>A1</a>
<b>B1</b>
<c>C1</c>
<d>D<e>E</e></d>
<b>B2</b>
<c>C2</c>
'''

selector = Selector(text=htmlText, type="html")

print("========== 例4-2-14 ==========")

expressions = [
    "//a/preceding-sibling::*",
    "//b/preceding-sibling::*[position()=1]",
    "//b[position()=2]/preceding-sibling::*",
    "//b[position()=2]/preceding-sibling::*[position()=1]"
]

for i, expr in enumerate(expressions, 1):
    s = selector.xpath(expr)
    print(f"\n{i}. XPath：{expr}")
    print("匹配数量：", len(s))
    print("提取结果：", s.extract())
