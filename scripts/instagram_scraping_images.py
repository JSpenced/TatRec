import csv
import random
import time
import os
from instaloader import Instaloader, Profile, ProfileNotExistsException, ConnectionException
from pathlib import Path

# Change if the data directory or script directories change
data_dir = Path("/Users/bigtyme/data/raw/instagram/chicago")
script_dir = Path("/Users/bigtyme/Dropbox/Insight/Project/scripts/")
max_posts = 50


def scrape_instagram_profile_posts(session: Instaloader, profile: str, max_posts: int = 20) -> None:
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


# Load instagram credentials from file to hide from repository (only loads first credentials)
with open(script_dir / ".insta-credentials") as csvfile:
    account_reader = csv.reader(csvfile, delimiter=',')
    first_row = next(account_reader)
    insta_user = first_row[0]
    insta_pass = first_row[1]

# Load artists instagram handles from file
with open(script_dir / "toronto_artists.csv") as csvfile:
    artist_reader = csv.reader(csvfile, delimiter=',')
    # (# at beginning of artist name means artist already dl'ed)
    artist_names = [artist[0] for artist in artist_reader if artist[0][0] != '#']

# change directory so saves to the data directory since can't be specified in instaloader
os.chdir(data_dir)
# Setup the scraper and only download images, tags, and text from posts
insta_sess = Instaloader(quiet=True, download_comments=False, download_pictures=True,
                         download_videos=False, download_video_thumbnails=False,
                         download_geotags=False)
# insta_sess.login(insta_user, insta_pass)
insta_sess.load_session_from_file("Mspencer02")

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
