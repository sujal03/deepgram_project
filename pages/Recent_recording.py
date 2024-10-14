import streamlit as st
import os
# Title of the app
st.title("Recent Voice Recording")


# Display the audio player
try:
    path=os.getcwd()+'/'+'cleaned_audio.wav'
    st.audio(path, format='wav/mp3')  # Change format based on the uploaded file type
except:
    st.write("No recent recording available.")


