from multiprocessing import current_process
import os
import requests
import shutil
from pytube import YouTube


def download_media_from_url(media_url: str):
    media_name = media_url.split("/")[-1]
    result = requests.get(media_url, stream=True)

    if result.status_code == 200:
        current_directory = __create_download_directory()

        result.raw.decode_content = True
        local_path = os.path.join(current_directory, media_name)
        with open(local_path, 'wb+') as destination:
            shutil.copyfileobj(result.raw, destination)

        return local_path, media_name
    else:
        raise Exception(f'Image {media_name} cannot be downloaded.')

def download_video_from_youtube(video_url: str):
    try: 
        youtube_video = YouTube(video_url)
    except:
        raise Exception(f'Video {video_url} cannot be downloaded.')

    video = youtube_video.streams.get_highest_resolution()
    
    try:
        current_directory = __create_download_directory()
        video.download(current_directory) 
    except: 
        raise Exception(f'Video {video_url} cannot be downloaded.')

def __create_download_directory():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    current_directory = os.path.join(current_directory, 'downloads')
    if not os.path.exists(current_directory):
        os.makedirs(current_directory)

    return current_directory
