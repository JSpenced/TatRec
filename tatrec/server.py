from flask import render_template, request, flash, session
from werkzeug.utils import secure_filename
from app import app
import os
from tatrec.recognition import TatRecognizer
from tatrec.config import path_web_img

# Create paths to files
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
tat_recognizer = TatRecognizer()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


@app.route('/recommendations', methods=['GET', 'POST'])
def get_recs():
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
            img_folder_path = app.config['UPLOAD_FOLDER']
            img_full_path = os.path.join(img_folder_path, filename)
            for the_file in os.listdir(img_folder_path):
                file_path = os.path.join(img_folder_path, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            img_file.save(os.path.join(img_full_path))
            img_paths = tat_recognizer.get_tattoo_recs()
            (session['img_rec1'], session['img_rec2'], session['img_rec3'], session['img_rec4'],
             session['img_rec5']) = img_paths
            session['img_full_path'] = img_full_path
            return render_template("index.html", img_upload=img_full_path,
                                   img_rec1=session['img_rec1'], img_rec2=session['img_rec2'],
                                   img_rec3=session['img_rec3'], img_rec4=session['img_rec4'],
                                   img_rec5=session['img_rec5'])
    return render_template("index.html", img_upload=session['img_full_path'],
                           img_rec1=session['img_rec1'], img_rec2=session['img_rec2'],
                           img_rec3=session['img_rec3'], img_rec4=session['img_rec4'],
                           img_rec5=session['img_rec5'])


@app.route('/', methods=["GET", "POST"])
def home_page():
    img_default = path_web_img + "tattoos/chicano-default.jpg"
    img_rec1 = path_web_img + "tattoos/chicano-tat1.jpg"
    img_rec2 = path_web_img + "tattoos/chicano-tat2.jpg"
    img_rec3 = path_web_img + "tattoos/chicano-tat3.jpg"
    img_rec4 = path_web_img + "tattoos/chicano-tat4.jpg"
    img_rec5 = path_web_img + "tattoos/chicano-tat5.jpg"
    return render_template('index.html', img_upload=img_default, img_rec1=img_rec1,
                           img_rec2=img_rec2, img_rec3=img_rec3, img_rec4=img_rec4,
                           img_rec5=img_rec5)


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/
