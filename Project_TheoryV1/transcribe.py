import os
import shutil
import subprocess
import whisper
from datetime import datetime

# --- PATHS ---
BASE = os.path.expanduser("~/gdrive/drafting")
VOICE_MEMOS = f"{BASE}/voice_memos"
ARCHIVE_AUDIO = f"{BASE}/archived_memos"
TRANSCRIPTIONS = f"{BASE}/transcriptions"
MASTER_FILE = f"{TRANSCRIPTIONS}/master_transcription.txt"

def setup():
    for d in [VOICE_MEMOS, ARCHIVE_AUDIO, TRANSCRIPTIONS]:
        os.makedirs(d, exist_ok=True)

def process_audio():
    setup()
    # Find .m4a, .m4p, or .wav files
    audio_files = [f for f in os.listdir(VOICE_MEMOS) if f.lower().endswith(('.m4a', '.m4p', '.wav'))]
    if not audio_files:
        print("No new memos found.")
        return

    # 1. Convert everything to MP3 using ffmpeg
    temp_files = []
    print("Converting and merging audio...")
    for f in sorted(audio_files):
        input_path = os.path.join(VOICE_MEMOS, f)
        temp_mp3 = os.path.join(VOICE_MEMOS, f.rsplit('.', 1)[0] + "_temp.mp3")
        subprocess.run(['ffmpeg', '-i', input_path, '-acodec', 'libmp3lame', '-y', temp_mp3], capture_output=True)
        temp_files.append(temp_mp3)

    # 2. Transcribe locally
    model = whisper.load_model("base")
    new_text = ""
    for mp3 in temp_files:
        print(f"Transcribing {os.path.basename(mp3)}...")
        result = model.transcribe(mp3)
        new_text += f"\n\n[Recorded: {datetime.now().strftime('%Y-%m-%d %H:%M')}]\n" + result['text']

    # 3. Append to Master or Create New
    mode = "a" if os.path.exists(MASTER_FILE) else "w"
    with open(MASTER_FILE, mode) as f:
        f.write(new_text)

    # 4. Cleanup & Archive
    for f in audio_files:
        shutil.move(os.path.join(VOICE_MEMOS, f), os.path.join(ARCHIVE_AUDIO, f))
    for t in temp_files:
        os.remove(t)
    
    print(f"Transcription complete. Master updated at: {MASTER_FILE}")

if __name__ == "__main__":
    process_audio()