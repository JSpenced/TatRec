import os
import re
import csv
from pathlib import Path
from instaloader import Instaloader, Profile
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


# Instagram related scraping functions


def scrape_instagram_profile_posts(session: Instaloader, profile: str, max_posts: int = 50) -> None:
    """Scrapes specified number of posts from an instagram profile and save in the current working
    directory.

    Args
    ----------
    profile : instaloader Profile of specific public Instagram user id
    number : maximum number of posts to extract (can have multiple images per post)

    Returns
    -------
    None

    """
    counter = 0
    profile = Profile.from_username(session.context, profile)
    for post in profile.get_posts():
        session.download_post(post, target=profile.username)
        counter += 1
        if counter == max_posts:
            break


def scrape_instagram_hashtag_posts(session: Instaloader, hashtag: str, max_posts: int = 50) -> None:
    """Scrapes specified number of posts from an instagram profile and save in the current working
    directory.

    Args
    ----------
    profile : instaloader Profile of specific public Instagram user id
    number : maximum number of posts to extract (can have multiple images per post)

    Returns
    -------
    None

    """
    counter = 0
    profile = Profile.from_username(session.context, hashtag)
    for post in profile.get_posts():
        session.download_post(post, target=profile.username)
        counter += 1
        if counter == max_posts:
            break


def get_insta_creds(path, row=1):
    """Load instagram credentials from file to hide from repository. If multiple credentials in file,
    can select a row to extract (defaults to first row).

    Args
    ----------
    path : path to instagram credentials
    row : which row of the instagram credentials file to extract

    Returns
    -------
    insta_user : Instagram username
    insta_pass : Instagram password

    """
    with open(path) as csvfile:
        account_reader = csv.reader(csvfile, delimiter=',')
        extract_row = next(account_reader)
        for i in range(0, row - 1):
            extract_row = next(account_reader)
        insta_user = extract_row[0]
        insta_pass = extract_row[1]
        return insta_user, insta_pass


# Web related scraping functions


def scrape_web_images(url: str, save_dir: str = None, filename_prefix: str = "") -> None:
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
