This project is an AI-powered music composer that allows users to generate customized music tracks using AI. The project consists of two main components: a Jupyter notebook (model.ipynb) and a Streamlit web application (app.py).

Project Structure
app.py: This file contains the Streamlit web application that provides a user interface for generating music tracks.
model.ipynb: This Jupyter notebook contains the code for interacting with the Beatoven AI API to create and compose music tracks.
How It Works
API Configuration: Both app.py and model.ipynb configure the API key and base URL for the Beatoven AI API. They also set up the headers required for authentication.
TO RUN The File sucessfully please keep your api key from beatoven (sharing api key through git hub may cause misues )
if it is not available please contact us using mail-velagadinesh099@gmail.com

Track Initialization:

The create_track function sends a POST request to the API to initialize a new track based on a text prompt provided by the user. The function returns a track ID.
Track Composition:

The compose_track function sends a POST request to the API to start composing the track using the track ID. It can also accept optional audio and video files to influence the composition. The function returns a task ID.
Check Composition Status:

The check_task_status function polls the API to check the status of the composition task. Once the track is composed, it retrieves the track URL and any available stems (individual audio components).
Streamlit Application:

The Streamlit app provides a user interface where users can choose to generate music using a text prompt, with optional audio or video input. Users can select from sample prompts or enter their own. The app then calls the functions to create and compose the track, and displays the final track URL for playback and download.
Running the Project
To run the Streamlit application, execute the following command in the terminal:
streamlit run app.py
