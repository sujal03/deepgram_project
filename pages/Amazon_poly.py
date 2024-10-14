import streamlit as st
import boto3
from pydub import AudioSegment
from pydub.playback import play
import tempfile

# Set up Amazon Polly client
polly_client = boto3.Session(
    aws_access_key_id='AKIAWCZC54ZYCHBJ3TO3',
    aws_secret_access_key='g8YSDRUofjEJFTCbkVJvx7yznCOgiKZGJi+a+Bdn',
    region_name='eu-north-1'  # Example: 'us-west-2'
).client('polly')

# Streamlit App UI
st.title("Text to Speech with Amazon Polly")

# Text input
text_input = st.text_area("Enter text to convert to speech:")

# Select voice
voice_options = {
    "Joanna (Female, US)": "Joanna",
    "Matthew (Male, US)": "Matthew",
    "Brian (Male, British)": "Brian",
    "Amy (Female, British)": "Amy"
}
voice = st.selectbox("Select Voice", list(voice_options.keys()))

# Submit button
if st.button("Convert to Speech"):
    if text_input:
        # Call Amazon Polly to synthesize speech
        response = polly_client.synthesize_speech(
            Text=text_input,
            OutputFormat="mp3",
            VoiceId=voice_options[voice]
        )

        # Save the audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_audio_file.write(response['AudioStream'].read())
            temp_audio_path = temp_audio_file.name

        # Use pydub to play the audio
        st.audio(temp_audio_path)

    else:
        st.warning("Please enter text to convert.")

