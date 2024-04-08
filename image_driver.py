import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import urllib.parse
import json

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

def save_image_url(url, path):
    with open(path, 'a') as file:
        file.write(url + '\n')

def download_image(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

def process_url(url):
    # Go to the webpage
    driver.get(url)

    # Wait for the image to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'wow-image')))

    # Find all images and get their data-src and data-image-info attributes
    images = driver.find_elements(By.TAG_NAME, 'wow-image')
    for img in images:
        img_url = img.get_attribute('data-src')
        img_info = json.loads(img.get_attribute('data-image-info'))
        if img_url and img_info and not img_info['isLQIP']:
            # Replace the filename in the URL with the original one
            parsed_url = urllib.parse.urlparse(img_url)
            path_parts = parsed_url.path.split('/')
            path_parts[-1] = img_info['imageData']['uri']
            new_path = '/'.join(path_parts)
            full_img_url = urllib.parse.urlunparse(parsed_url._replace(path=new_path))

            # Save the image URL
            img_name = urllib.parse.unquote(os.path.basename(full_img_url))
            save_dir = os.path.join('data', 'hullnext', urllib.parse.urlparse(url).path.strip('/'), 'images')
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, 'image_urls.txt')
            save_image_url(full_img_url, save_path)
            

with open('links.txt', 'r') as file:
    for line in file:
        url = line.strip()
        process_url(url)

# Close the browser
driver.quit()