from transformers import MusicgenForConditionalGeneration, AutoProcessor
import scipy.io.wavfile
import torch
import os

# --- CONFIGURATION ---
# SAVES TO YOUR SENSE FOLDER NOW
PROJECT_FOLDER = r"C:\Aniketh\Coding\sense" 
FILENAME = "background_beat.wav"
SAVE_PATH = os.path.join(PROJECT_FOLDER, FILENAME)

MODEL_ID = "facebook/musicgen-small"

def generate_beat():
    print("\n" + "="*40)
    print("🎵 AI MUSIC STUDIO (MusicGen Small)")
    print("="*40)
    feeling = input("What vibe do you need? (e.g. 'Chill', 'Energetic', 'Mysterious'): ")

    print("\n🎧 Loading the Musician...")
    
    # 1. Load Model
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = MusicgenForConditionalGeneration.from_pretrained(MODEL_ID)
    
    # Use CPU (Intel Arc doesn't support CUDA for audio yet)
    model.to("cpu") 

    print(f"   Composing beat for: '{feeling}'...")

    # 2. The Prompt
    text_prompt = [f"lo-fi hip hop beat, ambient, rhythmic, repetitive, soothing, {feeling}"]
    
    # 3. Generate
    inputs = processor(
        text=text_prompt,
        padding=True,
        return_tensors="pt",
    ).to("cpu")

    # Generate approx 5 seconds
    audio_values = model.generate(**inputs, max_new_tokens=256)

    # 4. Save
    sampling_rate = model.config.audio_encoder.sampling_rate
    audio_data = audio_values[0, 0].numpy()
    
    scipy.io.wavfile.write(SAVE_PATH, rate=sampling_rate, data=audio_data)
    
    print(f"   ✅ Beat Saved to: {SAVE_PATH}")

if __name__ == "__main__":
    while True:
        generate_beat()
        print("\nReady for next track. (Ctrl+C to quit)")