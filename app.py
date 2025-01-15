import streamlit as st
import requests
import time
import os

# API Configuration
API_KEY = '**************'  # Replace with your actual API key
BASE_URL = 'https://public-api.beatoven.ai/api/v1'

# Headers for authentication
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

# Function to initialize a track
def create_track(prompt_text):
    endpoint = f'{BASE_URL}/tracks'
    payload = {
        "prompt": {
            "text": prompt_text
        }
    }
    try:
        response = requests.post(endpoint, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        track_id = data['tracks'][0]  # Extract track ID from the response
        return track_id
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to create track: {e}")
        return None

# Function to compose a track
def compose_track(track_id, format="wav", looping=False, audio_file_path=None, video_file_path=None):
    endpoint = f'{BASE_URL}/tracks/compose/{track_id}'
    payload = {
        "format": format,
        "looping": looping
    }
    files = {}

    if audio_file_path:
        files["audio_file"] = open(audio_file_path, "rb")
    if video_file_path:
        files["video_file"] = open(video_file_path, "rb")

    try:
        response = requests.post(endpoint, headers=HEADERS, json=payload, files=files)
        response.raise_for_status()
        data = response.json()
        task_id = data['task_id']  # Extract task ID from the response
        return task_id
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to compose track: {e}")
        return None

# Function to check composition status
def check_task_status(task_id):
    endpoint = f'{BASE_URL}/tasks/{task_id}'
    try:
        while True:
            response = requests.get(endpoint, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            status = data['status']
            if status == 'composed':
                # Track composed successfully
                track_url = data['meta']['track_url']
                return track_url
            elif status in ['composing', 'running']:
                # Continue polling
                time.sleep(5)
            else:
                st.error("Task failed or encountered an issue.")
                return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to check task status: {e}")
        return None

# Streamlit Application
def main():
    st.title("AI-Powered Music Composer")
    st.write("Generate customized music tracks using AI!")

    # User chooses the mode of operation
    option = st.radio("Choose an option to generate music:", (
        "Generate music using text prompt",
        "Generate music using text prompt and audio input",
        "Generate music using text prompt and video input"
    ))

    if option == "Generate music using text prompt":
        # Sample prompts
        sample_prompts = [
            "30 seconds peaceful lo-fi chill hop track",
            "1-minute upbeat electronic dance music",
            "Calming background music for meditation",
            "Energetic rock track for a workout session",
        ]

        # User input for prompt
        prompt = st.selectbox("Choose a sample prompt or type your own:", sample_prompts)
        user_input = st.text_input("Or type your own prompt below:")
        if user_input.strip():
            prompt = user_input.strip()

        if st.button("Generate Music"):
            st.write("Initializing track...")
            track_id = create_track(prompt)
            if track_id:
                st.write("Starting composition...")
                task_id = compose_track(track_id)
                if task_id:
                    st.write("Composing your track. Please wait...")
                    track_url = check_task_status(task_id)
                    if track_url:
                        st.success("Your track is ready!")
                        st.audio(track_url, format="audio/wav", start_time=0)
                        st.write(f"[Download Track]({track_url})")

    
# Run the Streamlit app
if __name__ == "__main__":
    main()
