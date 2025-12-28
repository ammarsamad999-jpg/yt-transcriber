from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "YT Transcriber Running!"

@app.route("/transcribe", methods=["POST","OPTIONS"])
def transcribe():
    data = request.json
    url = data.get("url")

    if not url:
        return {"error": "YouTube URL missing"}, 400

    subprocess.run(
        f'yt-dlp -x --audio-format mp3 -o audio.mp3 "{url}"',
        shell=True,
        check=True
    )

    with open("audio.mp3", "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    return {"text": result.text}


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
