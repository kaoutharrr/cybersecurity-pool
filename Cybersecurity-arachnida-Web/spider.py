#!/usr/bin/env python3

import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


def is_image(url: str) -> bool:
    return url.lower().endswith(ALLOWED_EXTENSIONS)


def save_image(img_url: str, path: str):
    try:
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()

        filename = os.path.basename(urlparse(img_url).path)
        if not filename:
            return

        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(path, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"[+] Downloaded {filename}")
    except Exception:
        pass


def crawl(url: str, depth: int, max_depth: int, path: str, visited: set):
    if depth > max_depth or url in visited:
        return

    visited.add(url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception:
        return

    soup = BeautifulSoup(response.text, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        img_url = urljoin(url, src)
        if is_image(img_url):
            save_image(img_url, path)

    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue

        next_url = urljoin(url, href)
        crawl(next_url, depth + 1, max_depth, path, visited)


def main():
    parser = argparse.ArgumentParser(description="Spider image downloader")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-r", action="store_true", help="Recursive download")
    parser.add_argument("-l", type=int, default=5, help="Max depth level (default: 5)")
    parser.add_argument("-p", default="./data/", help="Download path")

    args = parser.parse_args()

    visited = set()

    if args.r:
        crawl(args.url, 0, args.l, args.p, visited)
    else:
        crawl(args.url, 0, 0, args.p, visited)


if __name__ == "__main__":
    main()
