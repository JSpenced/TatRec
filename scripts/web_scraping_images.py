import re
import csv
import os
from pathlib import Path
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def scrape_images(url: str, save_dir: str = None, filename_prefix: str = "") -> None:
    """
    Scrapes all images from a single webpage and save in current directory.
    Input the webpage url. Optionally, a directory to save the images and a
    filename prefix.
    """

    if save_dir is None:
        save_dir = Path(os.getcwd())

    # Request webpage and parse it
    request = Request(url)
    soup = BeautifulSoup(urlopen(request), 'html.parser')

    # find all img tags and extract the image url into a list for easy dl'ing
    img_tags = soup.find_all('img')
    urls = []
    for img in img_tags:
        src = img.get('data-src')
        if src is not None:
            urls.append(src)

    # loop through img urls saving each one to disk
    img_counter = 1
    for img in urls:
        if img is not None:
            with open(save_dir / (filename_prefix + "-" + str(img_counter) + ".jpg"), 'wb') as f:
                f.write(urlopen(img).read())
                img_counter += 1


def extract_webpage_name(url: str) -> str:
    """Return webpage name before .com/net/info or None
    """
    match = re.search(r'//(?:www\.)?([\w\-]+)\.', url)
    if match is not None:
        return match.group(1)


data_dir = Path("/Users/bigtyme/data/raw")
script_dir = Path("/Users/bigtyme/Dropbox/Insight/Project/scripts/")
name_prefixes = []
sites = []

# load in csv that contains artist name and site to extract images
with open(script_dir / "scrape_sites.csv") as csvfile:
    sites_reader = csv.reader(csvfile, delimiter=',')
    # csv first row is a name of the tatooist and second row is url
    for row in sites_reader:
        # extact out webpage name to use as the shop name
        shop_name = extract_webpage_name(row[1])
        if shop_name is None:
            shop_name = "Unkwown"
        name_prefixes.append(shop_name + '-' + row[0])
        sites.append(row[1])

# scrape all images on each page and save to folder shopname-artistname
for i, site in enumerate(sites):
    print('Scraping site: ' + site)
    data_path = data_dir / name_prefixes[i]
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    scrape_images(site, data_path, name_prefixes[i])
