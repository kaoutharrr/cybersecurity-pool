#!/usr/bin/env python3
import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

def is_image(url: str) -> bool:
    return url.lower().endswith(ALLOWED_EXTENSIONS)

def save_image(img_url: str, path: str, downloaded: set):
    if img_url in downloaded:
        return
    
    try:
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        
        filename = os.path.basename(urlparse(img_url).path)
        
        # Generate filename if empty
        if not filename or not is_image(filename):
            filename = f"image_{len(downloaded)}.jpg"
        
        os.makedirs(path, exist_ok=True)
        
        # Handle duplicate filenames
        filepath = os.path.join(path, filename)
        counter = 1
        while os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            filepath = os.path.join(path, f"{name}_{counter}{ext}")
            counter += 1
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        downloaded.add(img_url)
        print(f"[+] Downloaded {filename}")
        
    except Exception as e:
        print(f"[!] Error: {e}")

def crawl(url: str, depth: int, max_depth: int, path: str, visited: set, downloaded: set, base_domain: str = None):
    if depth > max_depth or url in visited:
        return
    
    if base_domain is None:
        base_domain = urlparse(url).netloc
    

    if urlparse(url).netloc != base_domain:
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
            save_image(img_url, path, downloaded)
    

    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue
        next_url = urljoin(url, href)

        if urlparse(next_url).netloc == base_domain:
            crawl(next_url, depth + 1, max_depth, path, visited, downloaded, base_domain)

def main():
    parser = argparse.ArgumentParser(description="Spider image downloader")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-r", action="store_true", help="Recursive download")
    parser.add_argument("-l", type=int, default=5, help="Max depth level (default: 5)")
    parser.add_argument("-p", default="./data/", help="Download path")
    parser.add_argument("-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    visited = set()
    downloaded = set()
    
    if args.r:
        crawl(args.url, 0, args.l, args.p, visited, downloaded)
    else:
        crawl(args.url, 0, 0, args.p, visited, downloaded)

if __name__ == "__main__":
    main()