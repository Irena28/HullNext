import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import urllib.parse

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

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
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))

    # Find all images and get their src attribute
    images = driver.find_elements(By.TAG_NAME, 'img')
    for img in images:
        img_url = img.get_attribute('src')
        if img_url:
            # Download the image
            img_name = urllib.parse.unquote(os.path.basename(img_url))
            download_dir = os.path.join('data', 'hullnext', urllib.parse.urlparse(url).path.strip('/'), 'images')
            os.makedirs(download_dir, exist_ok=True)
            download_path = os.path.join(download_dir, img_name)
            download_image(img_url, download_path)

with open('links.txt', 'r') as file:
    for line in file:
        url = line.strip()
        process_url(url)

# Close the browser
driver.quit()