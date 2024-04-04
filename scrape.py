import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import time

# Define headers as a global variable
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def download_resource(url, target_folder, referer=None):
    headers = HEADERS.copy()
    if referer:
        headers['Referer'] = referer

    filename = os.path.basename(urllib.parse.urlparse(url).path)
    if not filename:
        filename = 'index.html'

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(os.path.join(target_folder, filename), 'wb') as f:
                f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f'Error for URL {url}: {e}')

def extract_links(soup, target_folder):
    links = soup.find_all('a')
    unique_links = set(link.get('href') for link in links if link.get('href'))
    with open(os.path.join(target_folder, 'links.txt'), 'w', encoding='utf-8') as f:
        for link in unique_links:
            f.write(link + '\n')

def download_images(soup, url, target_folder):
    for img in soup.find_all('img'):
        img_url = urllib.parse.urljoin(url, img.get('src'))
        if img_url:
            download_resource(img_url, target_folder, referer=url)

def extract_text(soup, target_folder):
    spans = soup.find_all('span', class_='wixui-rich-text__text')
    unique_text = set(span.get_text() for span in spans)
    with open(os.path.join(target_folder, 'text.txt'), 'w', encoding='utf-8') as f:
        for text in unique_text:
            f.write(text + '\n')

def download_website(url, target_folder):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        with open(os.path.join(target_folder, 'index.html'), 'wb') as f:
            f.write(soup.prettify().encode('utf-8'))

        extract_links(soup, target_folder)
        download_images(soup, url, target_folder)
        extract_text(soup, target_folder)

    except requests.exceptions.RequestException as e:
        print(f'Error for URL {url}: {e}')

def run():
    root_dir = './data/hullnext'
    with open('links.txt', 'r') as f:
        for line in f:
            url = line.strip()  # Remove any leading/trailing whitespace
            if url:
                path = urllib.parse.urlparse(url).path
                subdirectory = path.strip('/').split('/')[-1]
                target_directory = os.path.join(root_dir, subdirectory)
                download_website(url, target_directory)
run()