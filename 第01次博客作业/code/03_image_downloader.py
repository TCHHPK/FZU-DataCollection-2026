
"""
作业③：网页图片批量下载
功能：爬取福州大学新闻网“影像福大”页面的 JPG、JPEG、PNG 图片。
"""

import hashlib
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


URL = "https://news.fzu.edu.cn/yxfd.htm"

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "data" / "images"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

# 限制单个文件大小为 20 MB
MAX_SIZE = 20 * 1024 * 1024


def fetch_page():
    """通过 requests 获取目标网页。"""
    response = requests.get(URL, headers=HEADERS, timeout=20)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text


def extract_image_urls(page_html):
    """解析页面中 img 标签引用的图片地址。"""
    soup = BeautifulSoup(page_html, "html.parser")
    image_urls = set()

    for img in soup.find_all("img"):
        # 兼容普通图片与常见懒加载属性
        for attr in ("src", "data-src", "data-original"):
            source = img.get(attr)

            if not source:
                continue

            source = source.strip()

            if source.startswith(("data:", "blob:")):
                continue

            full_url = urljoin(URL, source)
            parsed = urlparse(full_url)

            if parsed.scheme not in ("http", "https"):
                continue

            # 去除 URL 中的锚点
            full_url = parsed._replace(fragment="").geturl()
            image_urls.add(full_url)

        # 支持 srcset 中的图片
        srcset = img.get("srcset", "")

        for candidate in srcset.split(","):
            parts = candidate.strip().split()

            if not parts:
                continue

            source = parts[0]

            if source.startswith(("data:", "blob:")):
                continue

            full_url = urljoin(URL, source)
            parsed = urlparse(full_url)

            if parsed.scheme in ("http", "https"):
                image_urls.add(
                    parsed._replace(fragment="").geturl()
                )

    return sorted(image_urls)


def detect_image_type(data):
    """通过文件头识别 JPEG 或 PNG 格式。"""
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"

    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"

    return None


def download_image(session, image_url, index):
    """下载并验证单张图片。"""
    try:
        with session.get(
            image_url,
            timeout=20,
            stream=True,
            headers={"Referer": URL}
        ) as response:

            response.raise_for_status()

            content = bytearray()

            for chunk in response.iter_content(chunk_size=8192):
                if not chunk:
                    continue

                content.extend(chunk)

                if len(content) > MAX_SIZE:
                    print(f"[跳过] 图片超过 20 MB：{image_url}")
                    return False

        image_data = bytes(content)
        extension = detect_image_type(image_data)

        if extension is None:
            print(f"[跳过] 非 JPEG/PNG：{image_url}")
            return False

        # 使用内容哈希判断重复图片
        digest = hashlib.sha256(image_data).hexdigest()
        filename = f"image_{digest[:16]}{extension}"
        file_path = IMAGE_DIR / filename

        if file_path.exists():
            print(f"[重复] {filename}")
            return False

        file_path.write_bytes(image_data)

        print(
            f"[成功 {index}] {filename} "
            f"({len(image_data) / 1024:.1f} KB)"
        )
        return True

    except requests.RequestException as error:
        print(f"[失败] {image_url}：{error}")
        return False


def main():
    """执行图片提取和批量下载。"""
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("福州大学新闻网图片爬虫")
    print(f"目标网址：{URL}")
    print("=" * 60)

    try:
        page_html = fetch_page()
    except requests.RequestException as error:
        print(f"网页请求失败：{error}")
        return

    image_urls = extract_image_urls(page_html)
    print(f"\n发现 {len(image_urls)} 个图片资源地址。\n")

    if not image_urls:
        print("未找到图片，请检查网页结构。")
        return

    success_count = 0

    with requests.Session() as session:
        session.headers.update(HEADERS)

        for index, image_url in enumerate(image_urls, start=1):
            if download_image(session, image_url, index):
                success_count += 1

            # 控制下载频率，避免连续高频请求
            if index < len(image_urls):
                time.sleep(0.3)

    print("\n" + "=" * 60)
    print("爬取完成")
    print(f"发现资源：{len(image_urls)} 个")
    print(f"本次新下载：{success_count} 张")
    print(f"保存路径：{IMAGE_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
