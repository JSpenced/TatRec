#!/usr/bin/env python3
from flask import render_template, request, flash, session
from werkzeug.utils import secure_filename
from app import app
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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_index_page():
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


def load_user_from_json(path):
    with lzma.open(path + '.json.xz') as f:
        js = json.load(f)
        return (js['node']['owner']['username'], js['node']['owner']['edge_followed_by']['count'],
                js['node']['edge_media_preview_like']['count'])


def set_session_recs(rec_num, username, followers, likes, img_path):
    """ Set session variable for specific recommendation
    """
    session['user_rec' + str(rec_num+1)] = str(username)
    session['fols_rec' + str(rec_num+1)] = str(followers)
    session['likes_rec' + str(rec_num+1)] = str(likes)
    session['img_rec' + str(rec_num+1)] = img_path


def delete_files_from_folder(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


@app.route('/recommendations', methods=['GET', 'POST'])
def get_recs():
    """Return rendered web page with the recommended tattoo artists when a user clicks
    `Get tattoo Recs`
    """
    if request.method == 'POST':
        tat_dropdown = request.form.get('tatlist')
        # check if the post request has the file part
        img_folder_path = app.config['UPLOAD_FOLDER']
        if tat_dropdown == '':
            if 'file' not in request.files:
                flash("No file part, file didn't get sent to server. Please retry.")
                return get_index_page()
            img_file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if img_file.filename == '':
                flash('No selected file, please select a file to get your recs!')
                return get_index_page()
            if img_file and allowed_file(img_file.filename):
                filename = secure_filename(img_file.filename)
                img_full_path = os.path.join(img_folder_path, filename)
                delete_files_from_folder(img_folder_path)
            if img_full_path[-5:] == ".jpeg":
                img_full_path = img_full_path[:-5] + ".jpg"
            img_file.save(os.path.join(img_full_path))
        else:
            delete_files_from_folder(img_folder_path)
            img_name = 'tatrec--demo--' + tat_dropdown + '.jpg'
            print(os.path.join(img_folder_path, img_name))
            img_full_path = shutil.copy("./static/img/demo/" + img_name,
                                        os.path.join(img_folder_path, img_name))
            print(img_full_path)
        img_paths = tat_recognizer.get_tattoo_recs()
        session['img_full_path'] = img_full_path
        for i, path in enumerate(img_paths):
            if path[-3:] == 'UTC':
                username, followers, likes = load_user_from_json(path)
            else:
                username, followers, likes = load_user_from_json(path[:-2])
            set_session_recs(i, username, followers, likes, img_paths[i] + ".jpg")
        return get_index_page()
    return get_index_page()


@app.route('/', methods=["GET", "POST"])
def home_page():
    """Return rendered home page
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
def home():
    """Return the home page
    """
    return home_page()


@app.route('/about', methods=["GET", "POST"])
def about():
    """Return the about me page
    """
    return render_template("about.html")


@app.errorhandler(413)
def request_entity_too_large(error):
    flash('Max file size 2MB (reduce size or select a different file).')
    return get_index_page(), 413


# start the server with the 'run()' method
if __name__ == "__main__":
    # running on linux server need to change the host to 0.0.0.0
    if platform == "linux" or platform == "linux2":
        app.run(host="0.0.0.0", debug=True)
    elif platform == "darwin":
        app.run(debug=True)  # will run locally http://127.0.0.1:5000/
