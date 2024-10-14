import streamlit as st
import requests
import json
import os

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

os.environ['DG_API_KEY']='1b3c3b4929c6a4acaa3681c11290ebb07723d4bc'
filename = "output.wav"

# Title of the app
st.title("Text to Speech with Deepgram")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #4CAF50;
    }
    .button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #4CAF50;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Text input from the user
user_input = st.text_area("Enter text to convert to speech:", height=150)

# Button to convert text to speech
if st.button("Convert to Speech", key="convert"):
            SPEAK_OPTIONS = {"text": user_input}
            print(SPEAK_OPTIONS)
            try:
                # STEP 1: Create a Deepgram client using the API key from environment variables
                deepgram = DeepgramClient(api_key=os.getenv("DG_API_KEY"))

                # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
                options = SpeakOptions(
                    model="aura-asteria-en",
                    encoding="linear16",
                    container="wav"
                )

                # STEP 3: Call the save method on the speak property
                response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
                # print(response.to_json(indent=4))

            except Exception as e:
                print(f"Exception: {e}")

            st.audio(filename, format="audio/mp3")
            st.success("Speech generated successfully!")