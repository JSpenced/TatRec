from flask import Flask

UPLOAD_FOLDER = "/Users/bigtyme/Downloads/img_uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Create the application object
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
