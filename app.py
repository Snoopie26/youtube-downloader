from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h2>YouTube Audio Downloader 🎵</h2>
    <form action="/download" method="post">
        <input type="text" name="url" placeholder="Enter YouTube URL" required style="width:300px;">
        <button type="submit">Download Audio</button>
    </form>
    """

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return "No URL provided ❌"

    output_file = "audio.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
