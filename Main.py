from components.GetVideo import generate_video

if __name__ == "__main__":
    user_prompt = "Create a short but comprehensive video about IoT."
    video_file = generate_video(user_prompt, images_per_scene=1, resolution=(854, 480))

    if video_file:
        print("\nVideo generated successfully!")
       
    else:
        print("\nVideo generation failed. Check error logs above.")