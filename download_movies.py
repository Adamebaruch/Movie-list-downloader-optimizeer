import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from qbittorrentapi import Client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIGURATION ===
EXCEL_FILE = "/Users/adambaruch/Downloads/Baruch_Movies.xlsx"  # Update with your actual file path
MAX_SIZE_GB = 10  # Max file size in GB
QB_HOST = "localhost"  # Change if qBittorrent is on another machine
QB_PORT = 8080  # Web UI Port
QB_USERNAME = "Adam"  # Your qBittorrent username
QB_PASSWORD = "Baruch#1"  # Your qBittorrent password
DOWNLOAD_DIR = "/Users/adambaruch/OneDrive/Movies"  # Change to your OneDrive path

# === CONNECT TO QBittorrent ===
client = Client(host=QB_HOST, port=QB_PORT, username=QB_USERNAME, password=QB_PASSWORD)

# === READ MOVIE LIST FROM EXCEL ===
df = pd.read_excel(EXCEL_FILE)
movies = df.iloc[:, 0].tolist()  # Assuming movie titles are in the first column

# === Selenium Setup ===
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no browser UI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def search_torrent_site_piratebay(movie):
    """Search The Pirate Bay for a movie and return the best magnet link."""
    query = "+".join(movie.split())
    url = f"https://thepiratebay.org/search/{query}/1/"
    print(f"Searching URL on The Pirate Bay: {url}")  # Debug print

    try:
        driver.get(url)
        print(f"Successfully loaded {url}")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr"))
        )
        print(f"Page loaded successfully for {movie}")
    except Exception as e:
        print(f"Error loading page for {movie}: {e}")
        return None

    try:
        results = driver.find_elements(By.CSS_SELECTOR, "tr")
        print(f"Found {len(results)} results on The Pirate Bay for {movie}.")  # Debug print

        for result in results:
            try:
                title = result.find_element(By.CLASS_NAME, "detName")
                magnet = result.find_element(By.XPATH, './/a[@href]')
                size_text = result.find_element(By.CLASS_NAME, "size")

                if title and magnet and size_text:
                    title_text = title.text
                    magnet_link = magnet.get_attribute("href")
                    size_gb = convert_size_to_gb(size_text.text)

                    # Relax the filter criteria for size and format
                    if (".mp4" in title_text or ".mkv" in title_text or ".avi" in title_text):
                        print(f"Found magnet link for {movie}: {magnet_link}")  # Debug print
                        return magnet_link
                    else:
                        print(f"Skipping {title_text} because it doesn't match the filter.")  # Debug print
            except Exception as e:
                print(f"Error processing result on The Pirate Bay: {e}")
                continue
    except Exception as e:
        print(f"Error searching The Pirate Bay: {e}")
    return None

def search_torrent_site_1337x(movie):
    """Search 1337x for a movie and return the best magnet link."""
    query = "+".join(movie.split())
    url = f"https://1337x.to/search/{query}/1/"
    print(f"Searching URL on 1337x: {url}")  # Debug print

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to search for {movie} on 1337x, status code: {response.status_code}")  # Debug print
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("tr")
    print(f"Found {len(results)} results on 1337x for {movie}.")  # Debug print

    for result in results:
        try:
            title = result.find("a", class_="torrentname")
            magnet = result.find("a", href=True)
            size_text = result.find("td", class_="size")

            if title and magnet and size_text:
                title = title.text
                magnet = magnet["href"]
                size_gb = convert_size_to_gb(size_text.text)

                # Relax the filter criteria for size and format
                if (".mp4" in title or ".mkv" in title or ".avi" in title):
                    print(f"Found magnet link for {movie}: {magnet}")  # Debug print
                    return magnet
                else:
                    print(f"Skipping {title} because it doesn't match the filter.")  # Debug print
        except Exception as e:
            print(f"Error processing result on 1337x: {e}")
            continue
    return None

def convert_size_to_gb(size_text):
    """Convert size text (e.g., '2.3 GiB') to float in GB."""
    size_parts = size_text.split()
    if "GB" in size_parts:
        return float(size_parts[0])
    elif "MB" in size_parts:
        return float(size_parts[0]) / 1024
    return 999  # Default high value to skip unknown sizes

def download_torrents():
    """Loop through movies, search and download torrents."""
    for movie in movies:
        print(f"Searching for {movie}...")

        # Try The Pirate Bay first
        magnet = search_torrent_site_piratebay(movie)
        if magnet:
            print(f"Found magnet link for {movie} on The Pirate Bay.")
        else:
            print(f"No torrent found on The Pirate Bay for {movie}. Trying 1337x...")
            magnet = search_torrent_site_1337x(movie)
            if magnet:
                print(f"Found magnet link for {movie} on 1337x.")
            else:
                print(f"No suitable torrent found for {movie} on both sites.")
                continue

        # Add the torrent to qBittorrent
        print(f"Adding {movie} to qBittorrent...")
        client.torrents_add(urls=magnet, save_path=DOWNLOAD_DIR)
        
        time.sleep(random.uniform(1, 3))  # Avoid rate limiting

# Run the function
if __name__ == "__main__":
    download_torrents()

# Close the Selenium driver after use
driver.quit()