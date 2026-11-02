import csv
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import quote, urljoin, urlsplit
from concurrent.futures import ThreadPoolExecutor, as_completed

import urllib3
from bs4 import BeautifulSoup
from PIL import Image

# ===== 基本配置 =====
STUDENT_ID = "102402116"
KEYWORD = "书包"
PAGE_COUNT = int(STUDENT_ID[-1])       # 6页
MAX_IMAGES = int(STUDENT_ID[-3:])      # 116张
MAX_WORKERS = 4                        # 下载线程数

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "data" / "images"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9",
}

http = urllib3.PoolManager(
    maxsize=MAX_WORKERS,
    headers=HEADERS,
    retries=urllib3.Retry(
        total=2,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    ),
)


# ===== 生成搜索页面URL =====
def make_url(page):
    keyword = quote(KEYWORD.encode("gbk"))
    return (
        f"https://search.dangdang.com/"
        f"?key={keyword}&act=input"
        f"&page_index={page}&page_size=60"
    )


# ===== 解析商品图片 =====
def parse_page(page):
    url = make_url(page)
    print(f"[页面] 正在访问第 {page} 页：{url}", flush=True)

    try:
        response = http.request(
            "GET",
            url,
            timeout=urllib3.Timeout(connect=8, read=20),
        )

        if response.status != 200:
            print(f"[错误] 第 {page} 页 HTTP {response.status}")
            return []

        html = response.data.decode("gb18030", errors="replace")
        (ROOT / "data" / f"page_{page:02d}.html").write_text(
            html, encoding="utf-8"
        )

        soup = BeautifulSoup(html, "html.parser")
        products = []

        for li in soup.select("li"):
            a = li.select_one("a.pic")
            if a is None:
                continue

            img = a.find("img")
            if img is None:
                continue

            image_url = (
                img.get("data-original")
                or img.get("data-src")
                or img.get("src")
            )

            if not image_url:
                continue

            image_url = urljoin(url, image_url)

            if urlsplit(image_url).scheme not in ("http", "https"):
                continue

            if any(
                marker in image_url.lower()
                for marker in ("loading.gif", "blank.gif", "placeholder")
            ):
                continue

            title = (
                a.get("title")
                or img.get("alt")
                or "未知商品"
            ).strip()

            products.append({
                "page": page,
                "title": title,
                "url": image_url,
            })

        print(f"[页面] 第 {page} 页解析到 {len(products)} 张商品图片")
        return products

    except Exception as e:
        print(f"[错误] 第 {page} 页解析失败：{e}")
        return []


# ===== 多线程图片下载 =====
def download_image(item, index):
    filename = f"product_{index:03d}.jpg"
    filepath = IMAGE_DIR / filename

    try:
        if filepath.exists():
            with Image.open(filepath) as old:
                old.verify()
            return True, item, filename

        response = http.request(
            "GET",
            item["url"],
            timeout=urllib3.Timeout(connect=8, read=20),
        )

        if response.status != 200:
            raise ValueError(f"HTTP {response.status}")

        with Image.open(BytesIO(response.data)) as image:
            image.load()

            if min(image.size) < 60:
                raise ValueError("图片尺寸过小")

            image.convert("RGB").save(
                filepath, "JPEG", quality=90
            )

        print(f"[成功] {filename}", flush=True)
        return True, item, filename

    except Exception as e:
        print(f"[失败] {filename}：{e}", flush=True)
        return False, item, filename


# ===== 主程序 =====
def main():
    start = time.perf_counter()

    print("=" * 55)
    print("作业6：多线程商城商品图片爬虫")
    print(f"学号：{STUDENT_ID}")
    print(f"关键词：{KEYWORD}")
    print(f"爬取页码：1～{PAGE_COUNT}")
    print(f"目标图片数：{MAX_IMAGES}")
    print(f"下载线程数：{MAX_WORKERS}")
    print("=" * 55)

    all_products = []
    seen_urls = set()

    # 遍历搜索页并去重
    for page in range(1, PAGE_COUNT + 1):
        products = parse_page(page)

        for item in products:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                all_products.append(item)

        if page < PAGE_COUNT:
            time.sleep(1.5)

    print(f"\n共找到 {len(all_products)} 张不重复商品图片")

    if not all_products:
        print("没有解析到图片，请检查保存的HTML和网络访问情况。")
        return

    successes = []
    cursor = 0

    # 使用线程池批量下载，直到达到数量上限
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        while len(successes) < MAX_IMAGES and cursor < len(all_products):
            remaining = MAX_IMAGES - len(successes)
            batch = all_products[cursor:cursor + remaining]
            cursor += len(batch)

            futures = {
                pool.submit(download_image, item, index): item
                for index, item in enumerate(
                    batch, start=cursor - len(batch) + 1
                )
            }

            for future in as_completed(futures):
                ok, item, filename = future.result()
                if ok:
                    successes.append({
                        "filename": filename,
                        "page": item["page"],
                        "title": item["title"],
                        "url": item["url"],
                    })

    # 保存下载清单
    csv_path = ROOT / "data" / "images.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f, fieldnames=["filename", "page", "title", "url"]
        )
        writer.writeheader()
        writer.writerows(successes)

    elapsed = time.perf_counter() - start

    print("\n" + "=" * 55)
    print("多线程爬取结束")
    print(f"已访问页数：{PAGE_COUNT}")
    print(f"图片候选数：{len(all_products)}")
    print(f"成功下载数：{len(successes)}")
    print(f"目标图片数：{MAX_IMAGES}")
    print(f"运行耗时：{elapsed:.2f} 秒")
    print(f"图片保存路径：{IMAGE_DIR}")
    print("=" * 55)

    if len(successes) < MAX_IMAGES:
        print("注意：下载数量未达目标，请检查失败信息。")


if __name__ == "__main__":
    main()
