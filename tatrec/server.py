from flask import render_template, request, flash
from werkzeug.utils import secure_filename
from app import app
from pathlib import Path
import os

# Create paths to files
tattoos_path = Path("../data/raw/instagram/chicago/train/")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
img_default = "../static/img/tattoos/chicano-tat.jpg"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


@app.route('/recommendations', methods=['GET', 'POST'])
def get_tattoo_recs():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("index.html")
        img_file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if img_file.filename == '':
            flash('No selected file')
            return render_template("index.html")
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img_file.save(os.path.join(img_save_path))
            return render_template("index.html", img_upload=img_save_path)
    return


@app.route('/', methods=["GET", "POST"])
def home_page():
    return render_template('index.html', img_upload=img_default)  # render a template


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/
