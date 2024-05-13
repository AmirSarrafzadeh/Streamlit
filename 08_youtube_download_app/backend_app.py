from fastapi import FastAPI
from pytube import YouTube
from google.cloud import firestore

app = FastAPI()

# Initialize Firestore DB
db = firestore.Client()


@app.post("/download")
async def download_video(video_url: str):
    try:
        yt = YouTube(video_url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video:
            title = yt.title
            # Download video
            video.download()

            # Save to Firebase
            video_ref = db.collection('videos').document()
            video_ref.set({
                'title': title,
                'url': video_url
            })

            return {"message": "Video downloaded and added to Firebase.", "video_title": title}
        else:
            return {"error": "No video streams found."}
    except Exception as e:
        return {"error": str(e)}
