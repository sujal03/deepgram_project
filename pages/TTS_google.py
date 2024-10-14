import streamlit as st
from gtts import gTTS
import tempfile
import os

# Title of the app
st.title("Text to Speech with Google Gtts")

# Text input from the user
user_input = st.text_area("Enter text to convert to speech:")

# Button to convert text to speech
if st.button("Convert to Speech"):
    if user_input:
        # Convert text to speech
        tts = gTTS(text=user_input, lang='en')

        # Use a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file_name = tmp_file.name  # Save the temporary file name for later use
            tts.save(tmp_file_name)

        # Play the audio
        st.audio(tmp_file_name, format='audio/mp3')

        st.success("Speech generated successfully!")
    else:
        st.warning("Please enter some text.")
