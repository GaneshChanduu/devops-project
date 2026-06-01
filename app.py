from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)

# ✅ ENABLE CORS (VERY IMPORTANT for React)
CORS(app)

# 🔑 Your Jamendo Client ID
CLIENT_ID = "57c928e0"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/songs")
def get_songs():
    query = request.args.get("q", "")

    url = f"https://api.jamendo.com/v3.0/tracks/?client_id={CLIENT_ID}&format=json&limit=12&namesearch={query}"

    response = requests.get(url)
    data = response.json()

    songs = []

    for track in data["results"]:
        songs.append({
            "name": track.get("name"),
            "artist": track.get("artist_name"),
            "audio": track.get("audio"),
            "image": track.get("image")
        })

    return jsonify(songs)


if __name__ == "__main__":
    app.run()