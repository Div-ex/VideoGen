import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')


def search_google_images(query):
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