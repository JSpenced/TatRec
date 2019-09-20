import csv
import random
import time
import os
from typing import Union
from instaloader import Instaloader, Profile, ProfileNotExistsException, ConnectionException
from pathlib import Path

# Change if the data directory or script directories change
data_dir = Path("/Users/bigtyme/data/raw/instagram")
script_dir = Path("/Users/bigtyme/Dropbox/Insight/tatrec/scripts/")

# Load instagram credentials from file to hide from repository (only loads first credentials)
with open(script_dir / ".insta-credentials") as csvfile:
    account_reader = csv.reader(csvfile, delimiter=',')
    first_row = next(account_reader)
    insta_user = first_row[0]
    insta_pass = first_row[1]


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


def scrape_artists_from_file(filename_artists: Union[Path, str], save_path: Union[Path, str],
                             delimiter: str = ',', max_posts: int = 50) -> None:
    """Scrapes specific artists specified in csv file and save to data directory

    Args
    ----------
    filename_artists : csvfile with all the artists instagram profile names
    save_path : save path for downloaded images and comments
    delimiter : delimiter for csv file
    max_posts : maximum posts allowed

    Returns
    -------
    None

    """
    # Load artists instagram handles from file
    with open(script_dir / filename_artists) as csvfile:
        artist_reader = csv.reader(csvfile, delimiter=delimiter)
        # (# at beginning of artist name means artist already dl'ed)
        artist_names = [artist[0]
                        for artist in artist_reader if artist[0][0] != '#']

    # save current working directory and change to desired save directory since can't be specified
    # in instaloader
    cur_wd = os.getcwd()
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    os.chdir(save_path)

    # Setup the scraper and only download images, tags, and text from posts
    insta_sess = Instaloader(quiet=True, download_comments=False, download_pictures=True,
                             download_videos=False, download_video_thumbnails=False,
                             download_geotags=False)
    # login using load session file by running: instaloader -l username from command line and
    # inputting password
    insta_sess.login(insta_user, insta_pass)
    # insta_sess.load_session_from_file("Mspencer02")

    # loop through instagram handles downloading `max_posts` posts from each
    for insta_handle in artist_names:
        print("Starting to download profile: " + insta_handle)
        # Catches the error in case the artist profile doesn't exist anymore
        try:
            scrape_instagram_profile_posts(insta_sess, insta_handle, max_posts)
        except (ProfileNotExistsException, ConnectionException):
            print("Profile " + insta_handle + " doesn't exist.")
        # sleeps after each download of an artist for 1 to 3 minutes
        time.sleep(1 * 60 + random.random() * 120)

    # Change current working directory back to original working directory
    os.chdir(cur_wd)


scrape_artists_from_file("chicago_artists.csv", Path(data_dir / "test/"))
