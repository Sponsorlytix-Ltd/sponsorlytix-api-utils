import os
import requests
import shutil


def download_media(media_url: str):
    media_name = media_url.split("/")[-1]
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
