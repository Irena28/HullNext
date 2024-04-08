import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib.parse
import time

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

def take_screenshot(url, path):
    # Go to the webpage
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # Wait for 5 seconds

    # Set window size to a larger resolution
    driver.set_window_size(1920, 4320)

    # Take screenshot
    driver.save_screenshot(path)

with open('links.txt', 'r') as file:
    for line in file:
        url = line.strip()
        # Parse the URL to create a directory structure
        parsed_url = urllib.parse.urlparse(url)
        save_dir = os.path.join('data', 'hullnext', parsed_url.path.strip('/'), 'images')
        os.makedirs(save_dir, exist_ok=True)
        # Save the screenshot in the created directory
        screenshot_path = os.path.join(save_dir, 'screenshot.png')
        take_screenshot(url, screenshot_path)

# Close the browser
driver.quit()