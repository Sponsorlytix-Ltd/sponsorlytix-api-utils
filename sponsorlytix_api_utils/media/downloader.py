import os
import requests
import shutil
from pytube import YouTube


def download_media_from_url(media_url: str):
    media_name = media_url.split("/")[-1].split("?")[0]
    result = requests.get(media_url, stream=True)

    if result.status_code == 200:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        current_directory = os.path.join(current_directory, 'downloads')
        if not os.path.exists(current_directory):
            os.makedirs(current_directory)

        result.raw.decode_content = True
        local_path = os.path.join(current_directory, media_name)
        with open(local_path, 'wb+') as destination:
            shutil.copyfileobj(result.raw, destination)

        return local_path, media_name
    else:
        raise Exception(f'Image {media_name} cannot be downloaded.')



def download_youtube_video_from_url(video_url: str):

    file_name = video_url.split("/")[-1].split("?")[-1] +  '.mp4'

    current_directory = os.path.dirname(os.path.abspath(__file__))
    current_directory = os.path.join(current_directory, 'youtube_downloads')
    if not os.path.exists(current_directory):
        os.makedirs(current_directory)

    try:
        # object creation using YouTube
        # which was imported in the beginning
        yt = YouTube(video_url)

    except:
        print("Connection Error") #to handle exception

    # filters out all the files with "mp4" extension
    mp4files = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    try:
        # downloading the video
        file_path = mp4files.download(output_path=current_directory, filename= file_name, )
    except:
        print("Error!")
    print('Task Completed!')

    return file_path, file_name

