import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from scrape import download_resource

def traverse_folders(root_folder):
    for root, dirs, files in os.walk(root_folder):
        if 'index.html' in files:
            yield os.path.join(root, 'index.html')

def update_html_and_download_images(html_file_path):
    with open(html_file_path, 'r+', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        for img in soup.find_all('img'):
            img_url = img.get('src')
            if img_url:
                # Download the image
                img_name = os.path.basename(urlparse(img_url).path)
                img_folder = os.path.join(os.path.dirname(html_file_path), 'images')
                os.makedirs(img_folder, exist_ok=True)
                download_resource(img_url, img_folder)

                # Update the img tag's src to the local path
                img['src'] = os.path.join('images', img_name)

        # Write the updated HTML back to the file
        f.seek(0)
        f.write(str(soup))
        f.truncate()

# Traverse all folders and update each 'index.html'
for html_file in traverse_folders('data'):
    update_html_and_download_images(html_file)