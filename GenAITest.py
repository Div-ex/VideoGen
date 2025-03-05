import ollama
import requests
import re
import logging

PEXELS_API_KEY = "yGL3W2VuhNXeSMxcrToQK75sLOMXIoSOluc9G6eJLKIoGAvsywgBgFdZ"

def generate_script(prompt):
    try:
        result = ollama.chat(model='llama3.2:3b', messages=[
            {
                'role': 'system',
                'content': """Generate a video script in EXACT format:

KEYWORDS: 3-5 comma-separated keywords
SCRIPT:
- [Duration in seconds] [Narration]
- [Duration in seconds] [Narration]
(etc.)

The total duration of all 10 scenes should be around 60 seconds.
Provide at most 10 scenes. 
Provide maximum 10 scenes.
Example:

KEYWORDS: forest fire, melting glaciers, pollution
SCRIPT:
- 5.0: The flames are engulfing a dense forest
- 12.0: And large icebergs are collapsing into the ocean
- 20.0: Factories continue to emit dark smoke
... (etc.)

Now create a script for the following user prompt:
""",
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


def get_ollama_images(prompt, keywords):
    try:
        result = ollama.chat(model='llama3.2:3b', messages=[
            {
                'role': 'system',
                'content': f'Give me a single keyword for this input except for{keywords}',
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
    
def parse_script(output):
    """
    Parse the script output to extract keywords and a list of (duration, text).
    """
    if not output:
        return [], []

    keywords = []
    script = []

    keyword_match = re.search(r'KEYWORDS:\s*([^\n]+)', output, re.IGNORECASE)
    if keyword_match:
        keywords = [k.strip() for k in keyword_match.group(1).split(',') if k.strip()]

    script_lines = re.findall(r'-?\s*(\d+\.\d+):?\s*([^\n]+)', output)
    for duration, text in script_lines:
        try:
            duration = float(duration)
            # if 1 <= duration <= 20:
            script.append((duration, text.strip()))
        except ValueError:
            continue

    return keywords, script

# def fetch_pexels_images(keyword, num_images=1):
#     """
#     Fetch multiple images from Pexels for a given keyword.
#     Return list of image URLs. If not enough images found, returns fewer.
#     """
#     headers = {"Authorization": PEXELS_API_KEY}
#     params = {
#         "query": keyword,
#         "per_page": num_images,  
#         "page": 1
#     }

#     urls = []
#     try:
#         response = requests.get("https://api.pexels.com/v1/search",
#                                 headers=headers,
#                                 params=params,
#                                 timeout=15)
#         if response.status_code == 200:
#             data = response.json()
#             for photo in data.get('photos', []):
#                 urls.append(photo['src']['large'])
#         return urls
#     except Exception as e:
#         logging.error(f"Image fetch error: {str(e)}")
#         return urls
    


# raw_output = generate_script("History of fascism")
# clean_output = re.sub(r'http\S+', '', raw_output)
# clean_output = re.sub(r'.*(KEYWORDS:)', r'KEYWORDS:', clean_output, flags=re.DOTALL)
# print("\nthis",clean_output,"\n")
# keywords, script = parse_script(clean_output)
# print(keywords)
# print(script)

# keywords, script = parse_script(clean_output)
# if not script:
#         logging.error("No valid scenes in script.")
#             # return None
            
# print(keywords)

# all_clips = []
# scenet = ""
# for i, (duration, scene_text) in enumerate(script):
#     print(f"Scene {i+1}: {scene_text} ({duration}s)")
#     print(get_ollama_images(scene_text,keywords))
#     scenet = scene_text
# print(scenet)
# print (fetch_pexels_images(scenet, keywords))