import os
import requests
import cv2
import numpy as np
from PIL import Image
from gtts import gTTS
from transformers import pipeline
from moviepy.editor import *
from IPython.display import HTML, Audio, display
import textwrap
from io import BytesIO
import logging
import re
import os
from dotenv import load_dotenv

from components.GetVideo import generate_video
from tests.GenText import generate_script, parse_script, get_ollama_images
from tests.GetImgPex import fetch_pexels_images


load_dotenv()

# Configuration
PEXELS_API_KEY = os.getenv('PEXEL_API_KEY')



# PEXELS_API_KEY = ""
# HF_MODEL_NAME = "gpt2-medium"
logging.basicConfig(level=logging.INFO)



# def generate_script(prompt):
#     """
#     Generate a ~60-second video script with 3-5 keywords and multiple scenes.
#     Each scene line: '- duration: scene description'
#     """
#     try:
#         generator = pipeline(
#             "text-generation",
#             model=HF_MODEL_NAME,
#             device=0,         
#             pad_token_id=50256
#         )

#         system_prompt = """Generate a video script in EXACT format:

# KEYWORDS: 3-5 comma-separated keywords
# SCRIPT:
# - [Duration in seconds] [Scene description]
# - [Duration in seconds] [Scene description]
# (etc.)

# The total duration of all scenes should be around 60 seconds.
# Provide at least 6 scenes. Example:

# KEYWORDS: forest fire, melting glaciers, pollution
# SCRIPT:
# - 5.0: Flames engulfing a dense forest
# - 4.5: Large icebergs collapsing into ocean
# - 8.0: Factory smokestacks emitting dark smoke
# ... (etc.)

# Now create a script for the following user prompt:
# """

#         full_prompt = f"{system_prompt}\n{prompt}\n\nSCRIPT:"

#         response = generator(
#             full_prompt,
#             max_length=800,
#             num_return_sequences=1,
#             temperature=0.7,
#             do_sample=True,
#             truncation=True
#         )

#         raw_output = response[0]["generated_text"]

#         clean_output = re.sub(r'http\S+', '', raw_output)
#         clean_output = re.sub(r'.*(KEYWORDS:)', r'KEYWORDS:', clean_output, flags=re.DOTALL)
#         print("\nthis",raw_output,"\n")
#         return clean_output.strip()
#     except Exception as e:
#         logging.error(f"Script generation failed: {str(e)}")
#         return None

# # def parse_script(output):
#     """
#     Parse the script output to extract keywords and a list of (duration, text).
#     """
#     if not output:
#         return [], []

#     keywords = []
#     script = []

#     keyword_match = re.search(r'KEYWORDS:\s*([^\n]+)', output, re.IGNORECASE)
#     if keyword_match:
#         keywords = [k.strip() for k in keyword_match.group(1).split(',') if k.strip()]

#     script_lines = re.findall(r'-?\s*(\d+\.\d+):?\s*([^\n]+)', output)
#     for duration, text in script_lines:
#         try:
#             duration = float(duration)
#             if 1 <= duration <= 20:
#                 script.append((duration, text.strip()))
#         except ValueError:
#             continue

#     return keywords, script

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

#     urls = ["https://cdn.motor1.com/images/mgl/1ZEpmp/s1/pagani-zonda-760-roadster-diamante-verde.jpg"]
#     return urls
    # urls = []

    # try:
    #     response = requests.get("https://api.pexels.com/v1/search",
    #                             headers=headers,
    #                             params=params,
    #                             timeout=15)
    #     if response.status_code == 200:
    #         data = response.json()
    #         for photo in data.get('photos', []):
    #             urls.append(photo['src']['large'])
    #     return urls
    # except Exception as e:
    #     # logging.error(f"Image fetch error: {str(e)}")
        # return urls

# def create_clip_from_image(image_url, duration, text):
#     """
#     Create a single video clip from one image URL, with text overlay.
#     """
#     try:
#         response = requests.get(image_url, timeout=15)
#         img = Image.open(BytesIO(response.content)).convert("RGB")
#         img = img.resize((1280, 720))
#         img_np = np.array(img)

#         clip = ImageClip(img_np).set_duration(duration)

#         wrapped_text = textwrap.fill(text, width=40)
#         txt_clip = TextClip(
#             wrapped_text,
#             fontsize=28,
#             color="white",
#             font="DejaVu-Sans-Bold",
#             method="caption",
#             align="center",
#             stroke_color="black",
#             stroke_width=2
#         ).set_duration(duration).set_position(("center", "bottom"))

#         return CompositeVideoClip([clip, txt_clip])
#     except Exception as e:
#         logging.error(f"Clip creation from image failed: {str(e)}")
#         return None

# def create_clip_from_image(scene_text, keywords, images_per_scene = 1, output_audio_path="temp_audio.mp3", resolution = (854, 480)):
#     """
#     Create a single video clip from one image URL, with text overlay and TTS audio narration.
#     The duration of the clip is determined by the length of the generated audio narration.
#     """
    
#     if keywords:
#         primary_keyword = scene_text
#     else:
#         primary_keyword = "nature"  

    
#     image_url = fetch_pexels_images(primary_keyword, num_images=images_per_scene)

#     if not image_url:
#         logging.warning(f"No images found for {primary_keyword}, using fallback.")
#         return [ColorClip(size=resolution, color=(0,0,0), duration=duration)]
    
#     try:
#         # Generate TTS audio
#         text = scene_text
#         tts = gTTS(text)
#         tts.save(output_audio_path)
#         audio_clip = AudioFileClip(output_audio_path)
#         duration = audio_clip.duration  # Set video duration based on audio duration

#         # Fetch image
#         response = requests.get(image_url[0], timeout=15)
#         img = Image.open(BytesIO(response.content)).convert("RGB")
#         img = img.resize(resolution)  # Resize to 854x480 for better performance
#         img_np = np.array(img)
        
#         # Create video clip
#         clip = ImageClip(img_np).set_duration(duration)

#         # Create text overlay
#         wrapped_text = textwrap.fill(text, width=50)
#         txt_clip = TextClip(
#             wrapped_text,
#             fontsize=30,
#             color="white",
#             font="Arial",
#             method="label",
#             # align="center",
#             stroke_color="black",
#             stroke_width=1,
#         ).set_duration(duration).set_position(("center", "bottom"))
        
#         # Combine video and text overlay
#         video_clip = CompositeVideoClip([clip, txt_clip])
        
#         # Set audio narration to video
#         video_clip = video_clip.set_audio(audio_clip)
        
#         # video_clip.write_videofile("output_v.mp4", fps=24, codec='h264_nvenc', audio_codec='aac')

#         return video_clip
#     except Exception as e:
#         logging.error(f"Clip creation from image failed: {str(e)}")
#         return None

# def create_scene_clips(scene_text, duration, keywords, images_per_scene=1):
#     """
#     For each scene line, fetch multiple images for the best matching keyword
#     and create sub-clips which are then concatenated with crossfade.

#     - scene_text: The textual description for the scene
#     - duration: total duration of the scene
#     - keywords: list of keywords (can be used to refine fetch)
#     - images_per_scene: how many images to fetch for this scene
#     """
#     if keywords:
#         primary_keyword = scene_text
#     else:
#         primary_keyword = "nature"  

    
#     image_urls = fetch_pexels_images(primary_keyword, num_images=images_per_scene)

#     if not image_urls:
#         logging.warning(f"No images found for {primary_keyword}, using fallback.")
#         return [ColorClip(size=(1280,720), color=(0,0,0), duration=duration)]

#     subclip_duration = duration / len(image_urls)

#     sub_clips = []
#     for i, url in enumerate(image_urls):
#         sub_clip = create_clip_from_image(url, subclip_duration, scene_text)
#         if sub_clip:
#             if i > 0:
#                 sub_clip = sub_clip.crossfadein(1.0)  # 1s crossfade
#             sub_clips.append(sub_clip)

#     if len(sub_clips) == 1:
#         return sub_clips  

#     scene_clip = concatenate_videoclips(sub_clips, method="compose", padding=-1)
#     return [scene_clip]


# def generate_audio_narration(script):
#     """
#     generate tts. return audioclipfile
#     """

#     full_text = " ".join(scene_text for _, scene_text in script)
#     tts = gTTS(full_text)
#     audio_path = "narration.mp3"
#     tts.save(audio_path)
#     return AudioFileClip(audio_path)


# def generate_video(prompt, images_per_scene=1, resolution=(1280, 720)):
#     """
#     Full pipeline:
#       1) Generate script (approx 60s)
#       2) Parse it
#       3) For each scene, fetch images, create subclips with crossfade
#       4) Concatenate scene clips with crossfade
#       5) Generate TTS, overlay final audio
#       6) Write final video to disk
#     """
#     try:
#         raw_script = generate_script(prompt)
#         if not raw_script:
#             logging.error("No script generated.")
#             return None

#         keywords, script = parse_script(raw_script)
#         if not script:
#             logging.error("No valid scenes in script.")
#             logging.info(f"Parsed script: {script}")
#             return None

#         all_clips = []
#         for i, (duration, scene_text) in enumerate(script):
#             scene_clips = create_clip_from_image(
#                 scene_text=scene_text,
#                 # duration=duration,
#                 keywords=keywords,
#                 images_per_scene=images_per_scene,
#                 resolution=resolution,
#             )
#             print(scene_clips)
#             if not scene_clips:
#                 logging.error(f"Scene clips for '{scene_text}' are None.")
#                 continue 
#             # for idx, c in enumerate(scene_clips):
#             #     if i > 0 and idx == 0:
#             #         c = c.crossfadein(1.0)
#             #     all_clips.append(c)
#             scene_clips = scene_clips.crossfadein(1.0)
#             all_clips.append(scene_clips)
#         final_clip = concatenate_videoclips(all_clips, method="compose", padding=-1)

#         # narration = generate_audio_narration(script)

#         # final_clip = final_clip.set_audio(narration)

#         output_filename = "final_video.mp4"
#         final_clip.write_videofile(output_filename, fps=12, codec='hevc_nvenc', audio_codec='aac')

#         return output_filename
#     except Exception as e:
#         logging.error(f"Video generation error: {str(e)}")
#         return None


if __name__ == "__main__":
    user_prompt = "Create a short but comprehensive video about IoT."
    video_file = generate_video(user_prompt, images_per_scene=1, resolution=(854, 480))

    if video_file:
        print("\nVideo generated successfully!")
       
    else:
        print("\nVideo generation failed. Check error logs above.")