from flask import Flask

UPLOAD_FOLDER = "static/img/uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Create the application object
app = Flask(__name__)
app.secret_key = "tatrec_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
