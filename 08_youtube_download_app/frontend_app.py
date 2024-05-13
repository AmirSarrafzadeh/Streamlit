import streamlit as st
from pytube import YouTube


def download_youtube_video(video_url):
    try:
        yt = YouTube(video_url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video:
            print("Downloading:", yt.title)
            video.download()
            print("Download complete.")
        else:
            print("No video streams found.")
    except Exception as e:
        print("An error occurred:", str(e))


def main():
    st.title(':red[YouTube Video Downloader]')

    # Empty space for entering URL
    url = st.text_input("Enter Video URL:")
    # url = r"https://www.youtube.com/watch?v=QYbUWOMdglU&list=RDQYbUWOMdglU&start_radio=1"

    # Button to trigger download
    if st.button("Download"):
        # You can write the download logic here
        if url:
            download_youtube_video(url)
            print(f"Downloading: {url}")
        else:
            st.warning("Please enter a URL to download.")


if __name__ == "__main__":
    main()
