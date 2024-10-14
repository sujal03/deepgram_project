import streamlit as st
import os
import json
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

# Define your speech_to_text function here
def speech_to_text(audio_file):
    os.environ['DG_API_KEY']='1b3c3b4929c6a4acaa3681c11290ebb07723d4bc'
    # Placeholder for your speech-to-text implementation
    st.success("Getting text from audio file.")
    # You can process the audio file here
    # For example, load it using an audio processing library
    API_KEY = os.getenv("DG_API_KEY")
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        # with open(AUDIO_FILE, "rb") as file:
        #     buffer_data = file.read()
        buffer_data=audio_file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # STEP 4: Print the response
        response=response.to_json(indent=4)
        response_json = json.loads(response)
        transcript = response_json['results']['channels'][0]['alternatives'][0]['transcript']
        print(response)
        st.write(transcript)

    except Exception as e:
        st.write(f"Exception: {e}")

# Streamlit app title
st.title("Upload audio file and convert it to text...")

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])

# Check if a file has been uploaded
if uploaded_file is not None:
    st.audio(uploaded_file)  # Play the uploaded audio file
    st.write("File uploaded successfully!")
    
    # Call the speech_to_text function
    speech_to_text(uploaded_file)
else:
    st.info("Please upload an audio file to proceed.")

