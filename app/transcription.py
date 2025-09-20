# app/transcription.py

# app/transcription.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Hugging Face API key
HF_API_KEY = os.getenv("HF_API_KEY")
# This is the specific Whisper model we'll use from Hugging Face
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"


def get_transcript_from_audio(audio_bytes: bytes) -> str:
    """
    Calls the Hugging Face Inference API for Whisper to transcribe audio.
    """
    if not HF_API_KEY:
        raise ValueError("HF_API_KEY not found. Please set it in the .env file.")

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    print("🎤 Calling Whisper API for transcription...")
    
    try:
        response = requests.post(API_URL, headers=headers, data=audio_bytes)
        response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
        
        result = response.json()
        
        if "text" in result:
            return result["text"].strip()
        elif "error" in result:
            return f"Error from API: {result['error']}"
        else:
            return "Error: Unexpected API response format."

    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred with the Whisper API call: {e}")
        return f"Error: Could not connect to the transcription service. {e}"