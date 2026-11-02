
import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# 目标网址：2020 年软科中国大学排名
URL = "https://www.shanghairanking.cn/rankings/bcur/2020"

# 根据当前脚本位置定位项目目录
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "university_ranking.csv"


def fetch_page(url):
    """使用 requests 获取网页 HTML。"""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    response.encoding = "utf-8"

    return response.text


def parse_ranking(html):
    """使用 BeautifulSoup 解析大学排名表格。"""
    soup = BeautifulSoup(html, "html.parser")
    universities = []

    # 定位软科排名表格中的数据行
    rows = soup.select("table.rk-table tbody tr")

    for row in rows:
        cells = row.find_all("td")

        if len(cells) < 5:
            continue

        # 优先获取排名与学校中文名称
        rank_tag = cells[0].select_one(".ranking")
        name_tag = cells[1].select_one(".name-cn")

        rank = (
            rank_tag.get_text(strip=True)
            if rank_tag
            else cells[0].get_text(strip=True)
        )

        name = name_tag.get_text(strip=True) if name_tag else ""

        province = cells[2].get_text(strip=True)
        school_type = cells[3].get_text(strip=True)
        score = cells[4].get_text(strip=True)

        if not rank or not name:
            continue

        universities.append(
            [rank, name, province, school_type, score]
        )

    return universities


def print_ranking(universities):
    """在终端输出排名、学校、省市、类型和总分。"""
    print(f"{'排名':<6} {'学校名称':<16} {'省市':<8} {'类型':<8} {'总分'}")
    print("-" * 65)

    for rank, name, province, school_type, score in universities:
        print(
            f"{rank:<6} {name:<16} "
            f"{province:<8} {school_type:<8} {score}"
        )


def save_csv(universities):
    """将实际爬取的数据保存为 CSV 文件。"""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["排名", "学校名称", "省市", "学校类型", "总分"]
        )
        writer.writerows(universities)

    print(f"\nCSV 已保存：{OUTPUT_FILE}")


def main():
    try:
        html = fetch_page(URL)
        universities = parse_ranking(html)

        if not universities:
            print("未解析到排名数据，请检查网页结构。")
            return

        print_ranking(universities)
        print(f"\n成功爬取 {len(universities)} 所大学。")
        save_csv(universities)

    except requests.RequestException as error:
        print(f"网络请求失败：{error}")


if __name__ == "__main__":
    main()
