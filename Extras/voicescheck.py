import piper-tts

# Load a model (Download from Piper's GitHub)
model = piper.load_model("en_US-ryan-high.onnx")

# Generate speech
piper.synthesize(model, "This is an example narration.", "output.wav")