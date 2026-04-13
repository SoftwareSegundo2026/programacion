"""
Flask application for demonstrating database queries with the Chinook database.

This application sets up a Flask web server, connects to a SQLite database containing
music data (Chinook.db), and provides routes to display album information and perform
basic health checks.
"""

import os

from flask import Flask, render_template, jsonify, request
from sqlalchemy import text
from data.models import db, Album
from pprint import pprint as pp


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance", "Chinook.db")}'
db.init_app(app)

@app.route("/")
def hello():
    """Return a greeting message for the root route."""
    return "Hello from flask-example! 2026"

@app.get("/health")
def health():
    """Health check endpoint that returns OK status."""
    return "OK", 200

@app.route("/pepito")
def pepito():
    """Test route that returns a simple response."""
    return "Re OK", 200

@app.get("/albums/html")
def albums():
    """Render the albums page with data from the database."""
    albums = Album.query.all()
    resp = render_template("index.html", mis_albums=albums), 200
    return resp

@app.route("/albums")
def albums_json():
    """Return a JSON list of all albums."""
    albums = Album.query.all()
    albums_list = [
        {
            'AlbumId': album.AlbumId,
            'Title': album.Title,
            'ArtistId': album.ArtistId,
            'ArtistName': album.artist.Name if album.artist else None
        }
        for album in albums
    ]
    return jsonify(albums_list)

@app.route("/albums/<int:album_id>")
def get_album(album_id):
    """Return a JSON of a specific album."""
    album = Album.query.get_or_404(album_id)
    return jsonify({
        'AlbumId': album.AlbumId,
        'Title': album.Title,
        'ArtistId': album.ArtistId,
        'ArtistName': album.artist.Name if album.artist else None
    })

@app.route("/albums", methods=["POST"])
def create_album():
    """Create a new album."""
    data = request.get_json()
    if not data or 'Title' not in data or 'ArtistId' not in data:
        return jsonify({"error": "Title and ArtistId are required"}), 400
    new_album = Album()
    new_album.Title = data['Title']
    new_album.ArtistId = data['ArtistId']
    db.session.add(new_album)
    db.session.commit()
    return jsonify({
        'AlbumId': new_album.AlbumId,
        'Title': new_album.Title,
        'ArtistId': new_album.ArtistId,
        'ArtistName': new_album.artist.Name if new_album.artist else None
    }), 201

@app.route("/albums/<int:album_id>", methods=["PUT"])
def update_album(album_id):
    """Update an existing album."""
    album = Album.query.get_or_404(album_id)
    data = request.get_json()
    if 'Title' in data:
        album.Title = data['Title']
    if 'ArtistId' in data:
        album.ArtistId = data['ArtistId']
    db.session.commit()
    return jsonify({
        'AlbumId': album.AlbumId,
        'Title': album.Title,
        'ArtistId': album.ArtistId,
        'ArtistName': album.artist.Name if album.artist else None
    })

@app.route("/albums/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    """Delete an album."""
    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    return '', 204

@app.post("/pepito2")
def pepito2():
    """Test POST route that returns a simple response."""
    return "Re OK", 200

def main():
    """Main function to run the Flask application."""
    print("Hello from flask-example!")
    app.run(host="localhost", port=5000, debug=True)

@app.errorhandler(404)
def handle_404_error(e):
    return jsonify({
        "error": "Recurso no encontrado",
        "mensaje": "El ID solicitado no existe en nuestra base de datos",
        "status": 404
    }), 404

if __name__ == "__main__":
    main()
