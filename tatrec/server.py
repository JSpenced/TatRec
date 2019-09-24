from flask import render_template
from app import app

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route('/', methods=["GET", "POST"])
def home_page():
    return render_template('index.html')  # render a template


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True)  # will run locally http://127.0.0.1:5000/
