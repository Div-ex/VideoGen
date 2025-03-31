from flask import Flask, render_template, request, send_file
import os
from AudioAdd import generate_video

app = Flask(__name__)

# Ensure output directory exists
OUTPUT_VIDEO = "final_video.mp4"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        if not prompt:
            return render_template("index_F.html", message="Please enter a prompt!")

        # Generate video
        video_file = generate_video(prompt, images_per_scene=2)
        if video_file and os.path.exists(video_file):
            return render_template("index_F.html", video_ready=True, video_file=video_file)

        return render_template("index_F.html", message="Video generation failed. Try again!")

    return render_template("index_F.html", video_ready=False)

@app.route("/download")
def download():
    if os.path.exists(OUTPUT_VIDEO):
        return send_file(OUTPUT_VIDEO, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
