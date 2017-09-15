import os.path
import hashlib
import requests

headers = {'User-agent': "SubDB/1.0 (subgrab/1.0; http://github.com/RafayGhafoor/Subscene-Subtitle-Grabber)"}
languages = ('en', 'es', 'fr', 'it', 'nl', 'pl', 'pt', 'ro', 'sv', 'tr')
download_url = "http://api.thesubdb.com/?action=download"


def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def download(hash, filename, language='en'):
    r = requests.get(download_url + '&hash=' + hash + '&language=' + language, headers=headers)
    with open("Dog.srt", 'wb') as f:
        for chunk in r.iter_content(chunk_size=150):
            if chunk:
                f.write(chunk)


if __name__ == '__main__':
    hash = get_hash("A.Dogs.Purpose.2017.720p.WEB-DL.900MB.ShAaNiG.mkv")
    s = download(hash=hash, filename="A.Dogs.Purpose.2017.720p.WEB-DL.900MB.ShAaNiG.mkv", language='en')