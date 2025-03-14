from bs4 import BeautifulSoup
import requests
import os


# Trying to scrape the favicon from the working websites
def retrieve_icon(url):
    if not url.startswith('http'):
        url = 'https://' + url
    print(f"Retrieving favicon for {url}")
    try:
        response = requests.get(url, timeout = 5)
        response.raise_for_status() 
    except Exception as e:
        print(f"Failed to retrieve the webpage {url}: {e}. Skipping this website.")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')    
    link_icon = soup.find('link', rel='icon')
    if not link_icon:
        link_icon = soup.find('link', rel='shortcut icon')
        if not link_icon:
            print("Favicon not found.")
            return None

    favicon_url = link_icon['href']
    print(f"Found favicon at {favicon_url}")

    if not favicon_url.startswith('http'):
        favicon_url = requests.compat.urljoin(url, favicon_url)

    try:
        favicon_response = requests.get(favicon_url, timeout = 5)
        favicon_response.raise_for_status()
    except Exception as e:
        print(f"Failed to retrieve the favicon: {e}. Skipping the website.")
        return None

    data_folder = './data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    try:
        filename = os.path.join(data_folder, os.path.basename(f"{url}{favicon_url[len(favicon_url)-4:]}"))
        with open(filename, "wb") as f:
            f.write(favicon_response.content)
        print(f"Favicon saved as {filename}")
    except Exception as e:
        print(f"Error downloading favicon: {e}")
    



