#!/usr/bin/env python3
from flask import render_template, request, flash, session
from werkzeug.utils import secure_filename
from typing import Tuple, Any
from app import app, MAX_UPLOAD_SIZE
import os
import shutil
import json
import lzma
from sys import platform
from tatrec.recommender import TatRecommender
from tatrec.config import path_web_img

# Create paths to files
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
tat_recognizer = TatRecommender()


def allowed_file(filename: str) -> bool:
    """Check if the file is in allowed extensions.

    Args:
        filename: a filename

    Returns
        True for file in allowed extensions, False otherwise.

    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_index_page() -> Any:
    """Render the default homepage.

    Returns:
        A rendered homepage template.

    """
    return render_template("home.html", img_upload=session['img_full_path'],
                           img_rec1=session['img_rec1'], img_rec2=session['img_rec2'],
                           img_rec3=session['img_rec3'], img_rec4=session['img_rec4'],
                           img_rec5=session['img_rec5'], user_rec1=session['user_rec1'],
                           fols_rec1=session['fols_rec1'], user_rec2=session['user_rec2'],
                           fols_rec2=session['fols_rec2'], user_rec3=session['user_rec3'],
                           fols_rec3=session['fols_rec3'], user_rec4=session['user_rec4'],
                           fols_rec4=session['fols_rec4'], user_rec5=session['user_rec5'],
                           fols_rec5=session['fols_rec5'], likes_rec1=session['likes_rec1'],
                           likes_rec2=session['likes_rec2'], likes_rec3=session['likes_rec3'],
                           likes_rec4=session['likes_rec4'], likes_rec5=session['likes_rec5'])


def load_user_from_json(path: str) -> Tuple[str, int, int]:
    """Load a user's json file and extract username, followers, and likes.

    Args:
        path: full path to users json.xz file

    Returns:
        Username, followers, and post likes.

    """
    with lzma.open(path + '.json.xz') as f:
        js = json.load(f)
        return (js['node']['owner']['username'], js['node']['owner']['edge_followed_by']['count'],
                js['node']['edge_media_preview_like']['count'])


def set_session_recs(rec_num: int, username: str, followers: int, likes: int,
                     img_path: str) -> None:
    """Set flask session variables for specific recommendations.

    Args:
        rec_num: the recommendation number 1 to n
        username: instagram username
        followers: number of instagram followers
        likes: number of likes on post
        img_path: path to image recommendation

    """
    session['user_rec' + str(rec_num+1)] = str(username)
    session['fols_rec' + str(rec_num+1)] = str(followers)
    session['likes_rec' + str(rec_num+1)] = str(likes)
    session['img_rec' + str(rec_num+1)] = img_path


def delete_files_from_folder(path: str) -> None:
    """Delete all files in a specified folder.

    Args:
        path: path to folder to delete files

    """
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


@app.route('/recommendations', methods=['GET', 'POST'])
def get_recs() -> Any:
    """Return a rendered web page with the recommended tattoo artists when a user clicks
    `Get Recs`.

    Returns:
        A rendered recommendation webpage.

    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' in request.files:
            # get the tattoo demo dropdown list value
            tat_dropdown = request.form.get('tatlist')
            img_folder_path = app.config['UPLOAD_FOLDER']
            img_file = request.files['file']
            # if user does not select file flahes an error
            if img_file.filename == '' and tat_dropdown == '':
                flash('No selected file or dropdown selection, please select a file to get your recs!')
                return get_index_page()
            if img_file and allowed_file(img_file.filename):
                # generates a web secure filename
                filename = secure_filename(img_file.filename)
                img_full_path = os.path.join(img_folder_path, filename)
                delete_files_from_folder(img_folder_path)
                # model requires ".jpg" formatted files
                if img_full_path[-5:] == ".jpeg":
                    img_full_path = img_full_path[:-5] + ".jpg"
                img_file.save(os.path.join(img_full_path))
            # check if the dropdown menu was used
            elif tat_dropdown != '':
                delete_files_from_folder(img_folder_path)
                img_name = 'tatrec--demo--' + tat_dropdown + '.jpg'
                img_full_path = shutil.copy("./static/img/demo/" + img_name,
                                            os.path.join(img_folder_path, img_name))
        else:
            flash("There was an error with your selection, please retry!!")
            return get_index_page()
        # get image path of tattoo recommendations
        img_paths = tat_recognizer.get_tattoo_recs()
        session['img_full_path'] = img_full_path
        # setup images, followers, usernames, and likes variables for html
        for i, path in enumerate(img_paths):
            if path[-3:] == 'UTC':
                username, followers, likes = load_user_from_json(path)
            else:
                username, followers, likes = load_user_from_json(path[:-2])
            set_session_recs(i, username, followers, likes, img_paths[i] + ".jpg")
        return get_index_page()
    return get_index_page()


@app.route('/', methods=["GET", "POST"])
def home_page() -> Any:
    """Return the home page when website launched.

    Returns:
        Rendered homepage.

    """
    session['img_full_path'] = path_web_img + "homepage/chicano-input.jpg"
    likes = [1980, 2034, 2096, 1906, 2200]
    username = "yz_asencio_art"
    followers = 54019
    img_path = path_web_img + "homepage/chicano-img"
    for i in range(5):
        set_session_recs(i, username, followers, likes[i], img_path + str(i+1) + ".jpg")
    return get_index_page()


@app.route('/home', methods=["GET", "POST"])
def home() -> Any:
    """Return the home page on clicking home button.

    Returns:
        Rendered homepage.

    """
    return home_page()


@app.route('/about', methods=["GET", "POST"])
def about() -> Any:
    """Return the about me page.

    Returns:
        Rendered about me webpage.

    """
    return render_template("about.html")


@app.errorhandler(413)
def request_entity_too_large(error):
    """Used to flash an error when the user inputs an image that is to large.

    Args:
        error: input error

    Returns:
        Rendered home page with popup file size error.

    """
    flash('Max file size ' + str(MAX_UPLOAD_SIZE) + 'MB (reduce size or select a different file).')
    return get_index_page(), 413


# start the server with the 'run()' method
if __name__ == "__main__":
    # running on linux server need to change the host to 0.0.0.0
    if platform == "linux" or platform == "linux2":
        app.run(host="0.0.0.0", debug=True)
    elif platform == "darwin":
        app.run(debug=True)  # will run locally http://127.0.0.1:5000/
