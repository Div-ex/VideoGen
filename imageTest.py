from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

def search_images(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'searchType': 'image',
        'num': 5  # Adjust the number of results as needed
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        image_links = []
        if 'items' in results:
            for item in results['items']:
                image_links.append(item['link'])
        return image_links
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    images_links = search_images(query)
    if images_links:
        return jsonify({"images": images_links})
    else:
        return jsonify({"error": "Failed to fetch images"}), 500

if __name__ == '__main__':
    app.run(debug=True)
