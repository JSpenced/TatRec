import csv
from instaloader import Instaloader, Profile


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
