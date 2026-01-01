import torch
from transformers import pipeline
import generate_memory  # This MUST be in the same folder
import gc
import asyncio
import sys

# --- CONFIGURATION ---
LLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

def get_mode():
    print("\n" + "="*50)
    print("🩺 ANAMNESIS CONTROLLER")
    print("="*50)
    print("1. [Creative] Type a place")
    print("2. [Therapy]  Type a feeling")
    return input("Select 1 or 2: ").strip()

def load_brain():
    print("\n🧠 Loading Brain...")
    return pipeline("text-generation", model=LLM_MODEL, torch_dtype=torch.float16, device_map="auto")


def feeling_to_scene(feeling, chatbot):
    print(f"   Prescribing for '{feeling}'...")
    messages = [
        {"role": "system", "content": "You are an AI therapist. Suggest a calming physical place. Output ONLY the visual keywords."},
        {"role": "user", "content": f"I feel: {feeling}. Place keywords:"}
    ]
    output = chatbot(messages, max_new_tokens=60, do_sample=True, temperature=0.7)
    scene = output[0]['generated_text'][-1]['content'].replace('"', '').strip()
    
    print(f"   📍 Prescribed: {scene}")
    return scene

def run_generator():
    # 1. CLEAN MEMORY (Critical for Intel Arc)
    gc.collect()
    torch.cuda.empty_cache()

    # 2. CONSTRUCT PROMPT (Anti-Vortex enforced)
    final_prompt = f"equirectangular projection of {user_input} photorealistic, 8k, 360 panorama, seamless"
    voice_text = f"Welcome to this place. {user_input}. You are safe here."

    # 3. INJECT INTO YOUR SCRIPT
    print("\n🎨 Sending to Generator...")
    generate_memory.PROMPT = final_prompt
    generate_memory.VOICE_TEXT = voice_text
    
    # 4. EXECUTE
    # We call the functions from your working script directly
    img = generate_memory.generate_visuals()
    asyncio.run(generate_memory.generate_voice())
    print("\n✅ DONE! Check Unity.")

if __name__ == "__main__":
    mode = get_mode()
    brain = load_brain()

    if mode == "1":
        user_input = input("\nType a place (e.g. 'Forest'): ")
        del brain # Kill brain before image gen starts
        run_generator()
        
    elif mode == "2":
        feeling = input("\nType feeling (e.g. 'Anxious'): ")
        scene = feeling_to_scene(feeling, brain)
        del brain
        run_generator(scene)