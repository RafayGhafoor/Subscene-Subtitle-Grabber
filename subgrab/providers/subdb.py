import os.path
import hashlib
import requests

headers = {'User-agent': "SubDB/1.0 (subgrab/1.0; http://github.com/RafayGhafoor/Subscene-Subtitle-Grabber)"}
languages = ['en', 'es', 'fr', 'it', 'nl', 'pl', 'pt', 'ro', 'sv', 'tr']
search_url = "http://api.thesubdb.com/?action=search"
download_url = "'http://api.thesubdb.com/?action=download"


def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

hash = get_hash("Doctor Strange 2016.mkv")
r = requests.get(download_url + '&hash=')
