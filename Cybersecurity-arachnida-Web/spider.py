import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def parse_arguments():

    parser = argparse.ArgumentParser(prog='Spider', description='Arachnida: Spider')
    parser.add_argument("url")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-l", type=int, default=5)
    parser.add_argument("-p", default="./data/", help="Path to save files")
    return parser.parse_args()

def get_html(url):

    try:

        response = requests.get(url)
        response.raise_for_status()
        return(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html_text, base_url):
    soup = BeautifulSoup(html_text, 'html.parser')
    img_urls = []

    for img in soup.find_all('img'):
        url = img.get('src')
        if url:
            full_url = urljoin(base_url, url)
            extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
            if full_url.lower().endswith(extensions):
                img_urls.append(full_url)
    return img_urls


def download_imgs(img_urls, save_path):

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    for url in img_urls:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            filename = os.path.join(save_path, url.split("/")[-1])
            with open(filename, 'wb') as f:
                for chunck in response.iter_content(1024):
                    f.write(chunck)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

def get_links(html_text, base_url):

    soup = BeautifulSoup(html_text, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        full_url = urljoin(base_url, a['href'])
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.append(full_url)
    return links

visited = set()
def spider(url, current_level, max_level, save_path, recursive):
    
    if url in visited or current_level > max_level:
        return
    visited.add(url)
    print(f"Level {current_level}: Processing {url}")

    html_content = get_html(url)
    if html_content:
        imgs_urls = parse_html(html_content, url)
        download_imgs(imgs_urls, save_path)
    
        if recursive and current_level < max_level:
            soup = BeautifulSoup(html_content, 'html.parser')
            for a in soup.find_all('a', href=True):
                next_url= urljoin(url, a['href'])
                if urlparse(next_url).netloc == urlparse(url).netloc:
                    spider(next_url, current_level + 1, max_level, save_path, recursive)


def main():
    args = parse_arguments()
    spider(args.url, 0, args.l, args.p, args.r)

main()