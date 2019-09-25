import csv
import os
import sys
# Ensure tatrec package is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tatrec"))
from tatrec.scraping_funcs import scrape_web_images, extract_webpage_name
from tatrec.config import path_data_raw, path_scripts

path_data_web = path_data_raw / 'web'
name_prefixes = []
sites = []

# load in csv that contains artist name and site to extract images
with open(path_scripts / "scrape_sites.csv") as csvfile:
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
    data_path = path_data_web / name_prefixes[i]
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    scrape_web_images(site, data_path, name_prefixes[i])
