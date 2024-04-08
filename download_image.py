import requests
import os
import urllib.request

# Specify the path to the file
file_path = 'data/hullnext/activities-hull/images/image_urls.txt'
img_url = 'https://static.wixstatic.com/media/939d94fdfa86478b81e1edd1a9151e68.jpg/v1/fill/w_483,h_323,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/Mini%20Golf.jpg'

# Open the file and read the URLs
with open(file_path, 'r') as f:
    urls = f.read().splitlines()

# Specify the directory to save the images
save_dir = os.path.dirname(file_path)

# Define headers to make the request appear more "browser-like"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def download_images():

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Dnt': '1',
        'Priority': 'u=0, i',
        'Sec-Ch-Ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }   

    response = requests.get(img_url, stream=True, headers=headers)
    filename = img_url.split("/")[-1]

    # Save the file in the specified directory
    with open(os.path.join(save_dir, filename), 'wb') as out_file:
        out_file.write(response.content)

    print(f"Downloaded {filename}")

download_images()