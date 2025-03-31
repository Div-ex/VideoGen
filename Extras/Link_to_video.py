
import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image


def download_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        img = img.convert("RGB")
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)

        img = Image.open(img_byte_arr)
        img = np.array(img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img_bgr
    except Exception as e:
        print(f"Error downloading or processing image {url}: {e}")
        return None


def create_slideshow(image_urls, videofile, frame_rate=1, video_resolution=(1280, 720)):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(videofile, fourcc, frame_rate, video_resolution)

    for url in image_urls:
        try:
            img = download_image(url)
            if img is None:
                continue

            img_resized = cv2.resize(img, video_resolution)
            print(url)
            out.write(img_resized)
        except Exception as e:
            print(f"Error processing image {url}: {e}")

    out.release()

def main():
    image_urls = [
        "https://www.purina.in/sites/default/files/2023-05/feast.png",
        "https://www.bluecross.org.uk/sites/default/files/d8/styles/theme_feature_extra_large/public/2024-05/BX170007_Daisy-2024-04-23-0911_lpr.jpg.webp"
    ]
    videofile = 'slideshow.mp4'
    create_slideshow(image_urls, videofile)


if __name__ == "__main__":
    main()
