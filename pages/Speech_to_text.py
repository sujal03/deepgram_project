import streamlit as st
import streamlit.components.v1 as components

# Custom HTML for audio recording
audio_recorder_html = """
    <script>
        let mediaRecorder;
        let audioChunks = [];

        async function startRecording() {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.start();
            document.getElementById("status").innerHTML = "Recording...";
        }

        function stopRecording() {
            mediaRecorder.stop();
            document.getElementById("status").innerHTML = "Stopped Recording!";
            
            mediaRecorder.onstop = async function() {
                const audioBlob = new Blob(audioChunks, { 'type': 'audio/wav; codecs=0' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = audioUrl;
                a.download = 'recorded_audio.wav';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(audioUrl);
                audioChunks = [];
            };
        }
    </script>

    <button onclick="startRecording()">Start Recording</button>
    <button onclick="stopRecording()">Stop Recording</button>
    <p id="status"></p>
"""

st.title("Audio Recorder with Local Save")

# Display the HTML with JavaScript in Streamlit using components
components.html(audio_recorder_html, height=300)

# Instructions
st.write("Click 'Start Recording' to begin recording audio and 'Stop Recording' to save it locally.")
