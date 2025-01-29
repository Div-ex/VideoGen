from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import ollama
import requests
import os
from dotenv import load_dotenv
from Link_to_video import create_slideshow

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

# Initialize Flask app
app = Flask(__name__)
CORS(app)


def search_images(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    image_links = []


    for q in query:
        params = {
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'q': q,
            'searchType': 'image',
            'num': 1,
            
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json()
            if 'items' in results:
                for item in results['items']:
                    image_links.append(item['link'])
    
    if image_links:
        print(image_links)
        return image_links
    else:
        print("Failed to fetch images")
        return "Failed to fetch images"

def separate_script(script):
    # regular expression to identify  narrator
    narrator_pattern = r"Narrator: \"(.*?)\""
    narrator_pattern2 = r"Voiceover: \"(.*?)\""
    narrator_pattern3 = r"Host: \"(.*?)\""
    narrator_pattern4 = r"Narrator:\*\* \"(.*?)\""
    # converting tuple to string
    # narrator_pattern = "".join(narrator_pattern)

    # find narrator regex
    narrator_lines = re.findall(narrator_pattern, script)
    print("narrator")
    if narrator_lines == []:
            narrator_lines = re.findall(narrator_pattern2, script)
            print("voiceover")
    elif narrator_lines == []:
            narrator_lines = re.findall(narrator_pattern3, script)
            print("host")
    elif narrator_lines == []:
            narrator_lines = re.findall(narrator_pattern4, script)
            print("narrator**")

    print("wow",narrator_lines)
    
    # Replace the narrator lines in the script with an empty string to leave only other segments
    script_without_narrator = re.sub(narrator_pattern, "", script)

    # Split the remaining script by lines and filter out empty or whitespace-only lines
    other_segments = [line.strip() for line in script_without_narrator.splitlines() if line.strip()]

    # Return the separated lists
    return narrator_lines, other_segments
    

def get_ollama_response(prompt):
    try:
        
        result = ollama.chat(model='llama3.2:3b', messages=[
  {
    'role': 'system',
    'content': 'Give me a script for narrated 1 minute video.',
  },
  {
    'role': 'user',
    'content': prompt,
  },
])
        print(result['message']['content'])
        return result['message']['content']
    except Exception as e:
        return f"Exception occurred: {str(e)}"

def get_ollama_images(prompt):
    try:
        result = ollama.chat(model='llama3.2:3b', messages=[
  {
    'role': 'system',
    'content': 'Generate a just a single list of keywords. Output the list only, without any introduction or numbering. Each term in a new line',
  },
  {
    'role': 'user',
    'content': prompt,
  },
])
        print(result['message']['content'])
        return result['message']['content']
    except Exception as e:
        return f"Exception occurred: {str(e)}"

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
    image_terms_sent =  image_terms.replace("\n", "---")
    print(image_terms_list)
    if image_terms_list:
        image_links = search_images(image_terms_list)
        print("\n...\n")
    videofile = 'slideshow.avi'
    create_slideshow(image_links, videofile)
    return jsonify({"script" : " ".join(narrator_lines), "metadata" : "#".join(other_instructions), "image_terms" : image_terms_sent, "images" : image_links})

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Service is up!"})

if __name__ == "__main__":
    app.run()