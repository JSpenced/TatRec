#!/usr/bin/env python3
from flask import render_template, request, flash, session
from werkzeug.utils import secure_filename
from app import app
import os
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
    return render_template("index.html", img_upload=session['img_full_path'],
                           img_rec1=session['img_rec1'], img_rec2=session['img_rec2'],
                           img_rec3=session['img_rec3'], img_rec4=session['img_rec4'],
                           img_rec5=session['img_rec5'])
def load_user_from_json(path):
    with lzma.open(path + '.json.xz') as f:
        js = json.load(f)
        return (js['node']['owner']['username'], js['node']['owner']['edge_followed_by']['count'],
                js['node']['edge_media_preview_like']['count'])


@app.route('/recommendations', methods=['GET', 'POST'])
def get_recs():
    """Return rendered web page with the recommended tattoo artists when a user clicks
    `Get tattoo Recs`
    """
    if request.method == 'POST':
        # check if the post request has the file part
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
            img_folder_path = app.config['UPLOAD_FOLDER']
            img_full_path = os.path.join(img_folder_path, filename)
            for the_file in os.listdir(img_folder_path):
                file_path = os.path.join(img_folder_path, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            if img_full_path[-5:] == ".jpeg":
                img_full_path = img_full_path[:-5] + ".jpg"
            img_file.save(os.path.join(img_full_path))
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
    return get_index_page()


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
    session['img_full_path'] = path_web_img + "tattoos/chicano-default.jpg"
    session['img_rec1'] = path_web_img + "tattoos/chicano-tat1.jpg"
    session['img_rec2'] = path_web_img + "tattoos/chicano-tat2.jpg"
    session['img_rec3'] = path_web_img + "tattoos/chicano-tat3.jpg"
    session['img_rec4'] = path_web_img + "tattoos/chicano-tat4.jpg"
    session['img_rec5'] = path_web_img + "tattoos/chicano-tat5.jpg"
