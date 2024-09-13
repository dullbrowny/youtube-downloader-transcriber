import os
import subprocess
import whisper
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import tkinter as tk
from tkinter import filedialog

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_gdrive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_to_gdrive(file_path):
    creds = authenticate_gdrive()
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File uploaded successfully, File ID: {file.get('id')}")

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    transcript_file = file_path.replace('.mp3', '.txt')
    with open(transcript_file, 'w') as f:
        f.write(result['text'])
    return transcript_file

def download_videos(playlist_url, output_dir):
    command = f"yt-dlp -f bestaudio --extract-audio --audio-format mp3 {playlist_url} -o '{output_dir}/%(title)s.%(ext)s'"
    subprocess.run(command, shell=True)
    for file in os.listdir(output_dir):
        if file.endswith('.mp3'):
            transcript_file = transcribe_audio(os.path.join(output_dir, file))
            upload_to_gdrive(transcript_file)

def start_download():
    playlist_url = entry.get()
    output_dir = filedialog.askdirectory()
    if playlist_url and output_dir:
        download_videos(playlist_url, output_dir)
        label_status.config(text="Download, Transcription, and Upload Complete!")

# GUI Implementation
root = tk.Tk()
root.title("YouTube Playlist Downloader & Uploader")

label = tk.Label(root, text="Enter YouTube Playlist URL:")
label.pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

download_button = tk.Button(root, text="Download and Transcribe", command=start_download)
download_button.pack(pady=10)

label_status = tk.Label(root, text="")
label_status.pack(pady=20)

root.mainloop()

