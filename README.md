Essay Generation Workflow

transcribe.py
    Uses Open Whisper to transcribe audio files from iphone
    I use gdrive and rclone to manage the directory on the cloud and easily move files from recorder to local system
    This code also calls libraries for file management within the repository to avoid duplication
finalize.py
    This script takes the combined transcribed file and pings openrouter to generate an essay (with editor notes)
    the test file is simply used to confirm a working and proper connection to the assigned LLM - in this case claude-sonnet-3.5
