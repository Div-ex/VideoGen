import time
from flask import Flask, request, jsonify, render_template
import requests

# API_KEY = 'AIzaSyDRHJ3IJ5G2Y5mIUuDuSDVMvioUCUe-PMQ'
API_KEY = 'AIzaSyDQnA2PLE_UpjuzfvWwaZ4gj7wek-zntG0'
# SEARCH_ENGINE_ID = '14b3410c6ac474dd5'
SEARCH_ENGINE_ID = '424ec37b66c164e69'


def search_images(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    image_links = []
    
    for q in query:
        params = {
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'q': q,
            'searchType': 'image',
            'num': 1  # Adjust the number of results as needed
        }

        response = requests.get(url, params=params)
        print(response)
        if response.status_code == 200:
            results = response.json()
            if 'items' in results:
                for item in results['items']:
                    image_links.append(item['link'])
        time.sleep(1)
    
    if image_links:
        return image_links
    else:
        return None

print(search_images(["Alberto Ascari", "Fernando Alonso"]))