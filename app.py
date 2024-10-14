import streamlit as st
import sounddevice as sd
import wavio
from scipy.io.wavfile import write
import numpy as np
import os
    
if 'recording' not in st.session_state:
    st.session_state.recording =False
if "audio_data" not in st.session_state:
    st.session_state.audio_data = np.zeros(0)

# Parameters
fs = 44100  # Sample rate (44.1 kHz)
duration = 60 # Duration in seconds


# Function to start recording and save audio
def record_audio():
    # st.info("Recording started...")
    st.session_state.recording = True
    
    # Record audio for the given duration
    st.session_state.audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    # Wait until the recording is finished
    # sd.wait()
    
    st.write("Recording...")
    

def stop_recording():
    if st.session_state.recording:
        sd.stop()
        file_name = "recorded_audio.wav"
        # wavio.write(file_name, audio_data, fs, sampwidth=2)
        write(file_name, fs, st.session_state.audio_data)
        # st.write(f"Recording stopped.")
            # st.download_button("Download recorded audio", open(file_name, "rb"), file_name=file_name, mime="audio/wav")
        
# deepgram setup 
import os
import json
os.environ['DG_API_KEY']='1b3c3b4929c6a4acaa3681c11290ebb07723d4bc'


from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)




def speech_to_text():
    # Path to the audio file
    path=os.getcwd()+'/'+'cleaned_audio.wav'
    AUDIO_FILE = path
    API_KEY = os.getenv("DG_API_KEY")
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

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


# we got the audio file now we are going to create a new audio file and remove mute part of it
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def remove_silence(audio_file, silence_thresh=-50, min_silence_len=1000):
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)

    # Detect non-silent chunks (returns list of [start, end] in milliseconds)
    non_silent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # Combine all non-silent chunks into one audio segment
    non_silent_audio = AudioSegment.empty()
    for start, end in non_silent_ranges:
        non_silent_audio += audio[start:end]

    # Export the cleaned audio
    output_file = "cleaned_audio.wav"
    non_silent_audio.export(output_file, format="wav")
    # print(f"Processed audio saved as {output_file}")




# frontend
st.title("Speech to Text Generator:")
# Button to start recording
if st.button("Start Recording",key="start"):
    st.success("Recording started")
    record_audio()
    
if st.button("Stop Recording",key="stop"):
    st.success("Recording stopped")
    stop_recording()
    with st.spinner("waiting for text..."):
        remove_silence(os.getcwd()+'/'+'recorded_audio.wav')
        os.remove(os.getcwd()+'/'+'recorded_audio.wav')
        speech_to_text()
