import pyttsx3
from moviepy.editor import AudioFileClip

def generate_audio_narration(script, voice_id=None, rate=150):
    """
    Generate a TTS narration using pyttsx3 (offline TTS engine).
    Allows customization of voice and speaking rate.
    """
    engine = pyttsx3.init()
    
    # Set voice if provided
    if voice_id:
        engine.setProperty("voice", voice_id)
    
    # Set speech rate (default is 150)
    engine.setProperty("rate", rate)

    full_text = " ".join(scene_text for _, scene_text in script)
    
    audio_path = "narration.wav"
    engine.save_to_file(full_text, audio_path)
    engine.runAndWait()

    return AudioFileClip(audio_path)

# Example script input
script = [
    (1, "Once upon a time in a quiet village, there lived a young boy named Alex."),
    (2, "Alex loved exploring the forest near his home, discovering hidden paths and streams."),
]

# Generate narration with default voice
audio_clip = generate_audio_narration(script)
