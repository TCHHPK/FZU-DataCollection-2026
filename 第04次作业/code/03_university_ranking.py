import urllib.request
from bs4 import BeautifulSoup

url = "https://www.shanghairanking.cn/rankings/bcur/2020"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}

request = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(request) as response:
    html = response.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")

rows = soup.select("table tbody tr")

N = 16

print(
    f"{'排名':<6}"
    f"{'学校名称':<18}"
    f"{'省市':<10}"
    f"{'学校类型':<10}"
    f"{'总分':<10}"
)

count = 0

for row in rows:
    cols = row.find_all("td")

    if len(cols) < 5:
        continue

    # 排名
    rank = cols[0].get_text(strip=True)

    # 学校名称：只取中文名称所在的链接
    name_tag = cols[1].find("a")
    if name_tag:
        name = name_tag.get_text(strip=True)
    else:
        name = cols[1].get_text(strip=True)

    # 去掉英文名，只保留中文学校名
    name = "".join(
        ch for ch in name
        if "\u4e00" <= ch <= "\u9fff"
    )

    # 当前网页表格对应列
    province = cols[2].get_text(strip=True)
    school_type = cols[3].get_text(strip=True)
    score = cols[4].get_text(strip=True)

    print(
        f"{rank:<6}"
        f"{name:<18}"
        f"{province:<10}"
        f"{school_type:<10}"
        f"{score:<10}"
    )

    count += 1

    if count >= N:
        break