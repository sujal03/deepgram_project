import streamlit as st
import soundfile as sf
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import time
import tempfile
import os
from langchain.llms import Cohere

# Initialize recognizer
r = sr.Recognizer()

st.title("Voice based question answering system...")

# Function to record audio
def record_audio():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        st.write("Recording complete.")
    return audio

# Function to convert audio to text
def audio_to_text(audio):
    try:
        st.write("Converting speech to text...")
        text = r.recognize_google(audio)
        st.write("Conversion complete.")
        return text
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
    return None

# Function to simulate calling Cohere LLM (you will need to implement this)
def cohere_llm(text):
    # Placeholder for the Cohere LLM functionality
    os.environ['COHERE_API_KEY'] = 'C8buajOpTJaqrmm4cF9kKswk7RbRPnstQy0sQFjh'
    llm=Cohere()
    response=llm.invoke(text)
    return response

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        tts.save(tmp_file.name + ".mp3")
        return tmp_file.name + ".mp3"

# Button to start recording
if st.button("Start Recording"):
    st.session_state.audio = record_audio()

# Button to stop recording and process
if "audio" in st.session_state and st.button("Get Response..."):
    audio_data = st.session_state.audio

    # Convert audio to text
    text = audio_to_text(audio_data)

    # If text conversion is successful
    if text:
        st.write(f"Recognized text: {text}")
        st.write("Waiting for response from LLM...")

        # Pass the text to Cohere LLM (Simulated here)
        cohere_response = cohere_llm(text)

        # Convert Cohere LLM response to speech
        if cohere_response:
            st.write("Converting response to speech...")

            speech_file = text_to_speech(cohere_response)

            # Play the speech audio
            st.write("Here is the response:")
            st.audio(speech_file)
        else:
            st.write("Error: Could not process LLM response.")
    else:
        st.write("Error: No text received from speech recognition.")

# If still waiting for response, show waiting message
else:
    st.write("Waiting for response...")
    

