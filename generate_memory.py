import os
import asyncio
import edge_tts
from optimum.intel import OVStableDiffusionPipeline
from transformers import pipeline
from PIL import Image

# --- CONFIGURATION (These are the global variables the doctor will overwrite) ---
PROMPT = "equirectangular projection of a default peaceful scene, photorealistic, 8k, 360 panorama, seamless"
NEGATIVE_PROMPT = "distorted, blur, low quality, frame, border, watermark, text, nsfw,grid, split screen, tiled, collage, multiple views, diptych, triptych, frame, border, watermark, text, nsfw, distorted horizon, blurry, duplicate"
VOICE_TEXT = "Welcome to the default scene."

# --- AUTO-PATH FIX ---
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# --- GLOBAL MODEL CACHE (The Fix for Slow/Same Output) ---
# We load these once and reuse them every time the doctor calls the script.
global_pipe = None
global_depth_pipe = None

def load_stable_diffusion_pipe():
    global global_pipe
    if global_pipe is None:
        print("\n🎨 [1/3] Loading Image Generator (Cached)...")
        model_id = "OpenVINO/stable-diffusion-v1-5-fp16-ov"
        
        pipe = OVStableDiffusionPipeline.from_pretrained(
            model_id, 
            compile=False, 
            safety_checker=None 
        )
        pipe.to("GPU") # Forces it to use the Intel Arc GPU
        global_pipe = pipe
    return global_pipe

def load_depth_pipe():
    global global_depth_pipe
    if global_depth_pipe is None:
        global_depth_pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-small-hf")
    return global_depth_pipe


def generate_visuals():
    pipe = load_stable_diffusion_pipe()
    
    print(f"   Generating Image: '{PROMPT}'...") # <-- THIS IS THE KEY: It uses the global PROMPT variable
    image = pipe(
        PROMPT, 
        negative_prompt=NEGATIVE_PROMPT, 
        num_inference_steps=20, 
        height=512, 
        width=1024
    ).images[0]
    
    save_path = os.path.join(PROJECT_FOLDER, "memory_color.png")
    image.save(save_path)
    print(f"   ✅ Saved Image to: {save_path}")
    
    return image

def generate_depth(color_image):
    depth_pipe = load_depth_pipe()
    print("\n📐 [2/3] Calculating 3D Depth Map...")
    
    result = depth_pipe(color_image)
    depth_image = result["depth"]
    
    save_path = os.path.join(PROJECT_FOLDER, "memory_depth.png")
    depth_image.save(save_path)
    print(f"   ✅ Saved Depth Map to: {save_path}")

async def generate_voice():
    print("\n🎤 [3/3] Recording Therapist Voice...")
    
    voice = "en-US-JennyNeural" 
    communicate = edge_tts.Communicate(VOICE_TEXT, voice)
    
    save_path = os.path.join(PROJECT_FOLDER, "therapist_voice.mp3")
    await communicate.save(save_path)
    print(f"   ✅ Saved Audio to: {save_path}")

# This function is called by the doctor script
def run_full_generation():
    """
    Entry point function for the doctor script.
    Assumes PROMPT and VOICE_TEXT have been set externally by the doctor.
    """
    print("--- STARTING ANAMNESIS FACTORY ---")
    
    # 1. Generate the Look
    img = generate_visuals()
    
    # 2. Generate the Feel (Depth)
    generate_depth(img)
    
    # 3. Generate the Sound
    asyncio.run(generate_voice())
    
    print("\n--- GENERATION COMPLETE ---")

# We remove the 'if _name_ == "_main_":' block to prevent auto-running.