import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """ You are a YouTube Transcriber. Your job is to generate transcript text from a YouTube video and create a summary of all the important points."""

def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for i in transcript_text:
            transcript+=" " + i["text"]
        return transcript
    except Exception as k:
        raise k




def generate_gemini_content(transcript_text, prompt): #summarization
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcriber")
youtube_link=st.text_input("Enter your YouTube Video Link: ")
if youtube_link:
    video_id=youtube_link.split("v=")[1].split("&")[0]
    
    
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    transcipt_text=extract_transcript_details(youtube_link)
    if transcipt_text:
        summary= generate_gemini_content(transcipt_text, prompt)
        st.markdown("Summary: ")
        st.write(summary)
