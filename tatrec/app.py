from flask import Flask
from tatrec.config import path_web_upload_user

UPLOAD_FOLDER = path_web_upload_user
MAX_CONTENT_LENGTH = 2 * 1024 * 1024

# Create the application object
app = Flask(__name__)
app.secret_key = "tatrec_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
