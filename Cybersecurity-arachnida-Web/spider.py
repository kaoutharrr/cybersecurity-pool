import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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




args = parse_arguments()
html_xontent = get_html(args.url)
img_urls = parse_html(html_xontent, args.url)
download_imgs(img_urls, args.p)