import streamlit as st
import os
import subprocess
import tempfile

st.set_page_config(page_title="Video Processor", layout="centered")
st.title("🎬 Video Processor and Audio Extractor")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    st.video(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())
        input_path = temp_file.name
        base_name = os.path.splitext(os.path.basename(input_path))[0]

    # Extract Audio
    audio_path = f"{base_name}_audio.wav"
    st.info("Extracting audio...")
    subprocess.run(["ffmpeg", "-y", "-i", input_path, "-q:a", "0", "-map", "a", audio_path])
    st.success("Audio extracted!")

    # Convert to Reel Format
    reel_path = f"{base_name}_reel.mp4"
    st.info("Converting to vertical reel format (1080x1920)...")
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path, "-vf",
        "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        reel_path
    ])
    st.success("Reel format conversion complete!")

    # Optional: Chunking
    if st.checkbox("Split into 5-minute chunks"):
        chunk_dir = f"{base_name}_chunks"
        os.makedirs(chunk_dir, exist_ok=True)
        st.info("Splitting video...")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path, "-c", "copy", "-map", "0",
            "-segment_time", "300", "-f", "segment",
            os.path.join(chunk_dir, "chunk_%03d.mp4")
        ])
        st.success(f"Video split into chunks! Check folder: {chunk_dir}")
