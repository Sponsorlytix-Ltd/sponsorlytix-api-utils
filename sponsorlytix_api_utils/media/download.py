import requests
import shutil

def download_media(media_url : str):
    media_name = media_url.split("/")[-1]
    result = requests.get(media_url, stream = True)

    if result.status_code == 200:
        result.raw.decode_content = True
        
        with open(media_name, 'wb') as f:
            shutil.copyfileobj(result.raw, f)
    else:
        raise Exception(f'Image {media_name} cannot be downloaded.')
