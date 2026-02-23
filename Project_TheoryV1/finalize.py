import os
import shutil
from openai import OpenAI
from datetime import datetime

BASE = os.path.expanduser("~/gdrive/drafting")
TRANSCRIPTIONS = f"{BASE}/transcriptions"
ARCHIVE_TRANS = f"{TRANSCRIPTIONS}/archived_transcriptions"
MASTER_FILE = f"{TRANSCRIPTIONS}/master_transcription.txt"


api_key = os.environ.get("CLOUD_AI_API_KEY") #Fetch the key bashrc

if not api_key:
    print("CRITICAL ERROR: 'CLOUD_AI_API_KEY' not found in environment.")
    print("Please run: export CLOUD_AI_API_KEY='your-key-here' and try again.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "http://localhost", # Helps OpenRouter route the request
        "X-Title": "Arch Essay Tool",      # Identifies app in the dashboard
    }
)

def finalize_essay():
    if not os.path.exists(MASTER_FILE):
        print("No master transcription found to finalize.")
        return

    with open(MASTER_FILE, "r") as f:
        content = f.read()

    print("Synthesizing final draft with Cloud AI...")
    
    # Combined Prompt: Editor + Essayist logic
    prompt = (
        "You are a master essayist and developmental editor. Take the following raw thoughts. "
        "1. Structure them into a cohesive narrative essay. "
        "2. Include 'Editor Asides' in brackets where you suggest anecdotes or deeper research. "
        "3. Preserve the author's unique voice—do not use generic AI transitions."
        "4. Include syntax for readability in a .txt file"
    )

    response = client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet", # Best for human-like prose
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}]
    )

    final_draft = response.choices[0].message.content
    
    # Save the Final Draft
    timestamp = os.path.getmtime(MASTER_FILE)
    date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H%M')
    with open(f"{BASE}/FINAL_ESSAY_{date_str}.txt", "w") as f:
        f.write(final_draft)

    # Archive and Clean Up
    os.makedirs(ARCHIVE_TRANS, exist_ok=True)
    archive_path = f"{ARCHIVE_TRANS}/transcription_backup_{date_str}.txt"
    final_path = f"{BASE}/master_transcription"
    
    # Using rename for better compatibility with the Rclone mount
    os.rename(MASTER_FILE, archive_path)
    
    print(f"Success!")
    print(f"Draft saved to: {final_path}")
    print(f"Source archived to: {archive_path}")

if __name__ == "__main__":
    finalize_essay()