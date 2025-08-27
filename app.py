from flask import Flask, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ YouTube Audio Downloader is running! Use /download?url=VIDEO_URL"

@app.route("/download")
def download_audio():
    try:
        url = request.args.get("url")
        if not url:
            return "❌ Please provide a YouTube URL with ?url="

        yt = YouTube(url)

        # Get best audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Save as audio file
        filename = yt.title.replace(" ", "_") + ".mp4"
        audio_path = os.path.join("downloads", filename)

        os.makedirs("downloads", exist_ok=True)

        audio_stream.download(output_path="downloads", filename=filename)

        return send_file(audio_path, as_attachment=True)

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
