import os

from flask import Flask, render_template
from sqlalchemy import text
from data.models import db, Album
from pprint import pprint as pp


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance", "Chinook.db")}'
db.init_app(app)

with app.app_context():
    # result = db.session.execute(text("SELECT Title FROM Album"))
    result = Album.query.all()
    # my_albums = result.fetchall()
    my_albums = result
    # pp(my_albums)

@app.route("/")
def hello():
    return "Hello from flask-example! 2026"

@app.get("/health")
def health():
    return "OK", 200

@app.route("/pepito")
def pepito():
    return "Re OK", 200

@app.get("/albums")
def albums():
    resp = render_template("index.html", mis_albums=my_albums), 200
    # print(resp)
    return resp

@app.post("/pepito2")
def pepito2():
    return "Re OK", 200

def main():
    print("Hello from flask-example!")
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
