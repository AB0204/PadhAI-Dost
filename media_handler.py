import google.generativeai as genai
import time
import os

def upload_media(file_path, api_key, display_name="Uploaded Media"):
    """
    Uploads a media file (audio/video) to Google Gemini File API.
    Waits for the file to be processed and active.
    """
    if not api_key:
        raise ValueError("API Key not provided.")
    
    genai.configure(api_key=api_key)

    print(f"Uploading file: {file_path}")
    sample_file = genai.upload_file(path=file_path, display_name=display_name)
    
    print(f"Completed upload: {sample_file.uri}")

    # Check state and wait for it to become active
    while sample_file.state.name == "PROCESSING":
        print("Processing video/audio...")
        time.sleep(2)
        sample_file = genai.get_file(sample_file.name)

    if sample_file.state.name == "FAILED":
        raise ValueError("File processing failed.")

    print(f"File active: {sample_file.name}")
    return sample_file
