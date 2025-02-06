from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from Google_linker import search_google_images
from Pexel_linker import fetch_pexels_images

from GenAI_response import get_ollama_response, get_ollama_images
from Script_separate import separate_script

from Link_to_video import create_slideshow

app = Flask(__name__)

CORS(app)


@app.route('/')
def index():
    return render_template('chatBot.html')


@app.route("/api/prompt", methods=["POST"])
def prompt():

    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data['prompt']
    response = get_ollama_response(prompt)

    narrator_lines, other_instructions = separate_script(response)
    print(type(narrator_lines))
    image_terms = get_ollama_images("".join(narrator_lines))

    image_terms_list = image_terms.split("\n")
    image_terms_sent = image_terms.replace("\n", "---")
    print(image_terms_list)
    if image_terms_list:
        image_links = search_google_images(image_terms_list)
        # image_links = fetch_pexels_images(image_terms_list)

        print("\n...\n")
    videofile = 'slideshow.avi'
    create_slideshow(image_links, videofile)
    return jsonify({"script": " ".join(narrator_lines), "metadata": "#".join(other_instructions), "image_terms": image_terms_sent, "images": image_links})


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Service is up!"})


if __name__ == "__main__":
    app.run()
