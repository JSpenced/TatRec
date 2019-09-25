from flask import Flask
import os

UPLOAD_FOLDER = "static/img/uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Create the application object
app = Flask(__name__, template_folder=TMP_DIR)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
