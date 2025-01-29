import requests
import os
import time
import cv2
from dotenv import load_dotenv
load_dotenv()

# Configuration
API_KEY = os.getenv('PEXEL_API_KEY') 
IMAGES_PER_KEYWORD = 1 
REQUEST_DELAY = 1  # Delay between requests in seconds (avoid rate limiting)

# def download_image(url, file_path):
#     """Download and save an image from a given URL"""
#     for u in url:
#         try:
#             response = requests.get(url, stream=True)
#             if response.status_code == 200:
#                 with open(file_path, 'wb') as f:
#                     for chunk in response.iter_content(1024):
#                         f.write(chunk)
#                 return True
#         except Exception as e:
#             print(f"Error downloading image: {str(e)}")
#         return False

def fetch_pexels_images(KEYWORDS):
    headers = {"Authorization": API_KEY}
    
    photo_urls = []
    for keyword in KEYWORDS:
        print(f"\nSearching for '{keyword}' images...")
        
        # Fetch images from Pexels API
        response = requests.get(f"https://api.pexels.com/v1/search?query={keyword}&per_page={IMAGES_PER_KEYWORD}", headers=headers)
        print(response)
        # data = response.json()
        # print(data)
        if response.status_code == 200:
            data = response.json()
            for photo in data['photos']:
                print(photo['src']['original'])
                photo_urls.append(photo['src']['original']) # Save image URL
        else:
            print(f"Error fetching images for keyword '{keyword}': {response.status_code}")
        time.sleep(REQUEST_DELAY)
    print(photo_urls)
    return photo_urls

# if __name__ == "__main__":
#     if not API_KEY or API_KEY == "YOUR_API_KEY":
#         print("Please set your Pexels API key in the script")
#     else:
#         fetch_pexels_images()
#         print("\nImage download process completed!")