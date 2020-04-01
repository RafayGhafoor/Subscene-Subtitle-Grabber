import hashlib
import logging
import os.path

import requests


HEADERS = {
    "User-agent": "SubDB/1.0 (subgrab/1.0; http://github.com/RafayGhafoor/Subscene-Subtitle-Grabber)"
}
LANGUAGES = ("en", "es", "fr", "it", "nl", "pl", "pt", "ro", "sv", "tr")
DOWNLOAD_URL = "http://api.thesubdb.com/?action=download"
logger = logging.getLogger("subdb.py")


def get_hash(name):
    readsize = 64 * 1024
    with open(name, "rb") as f:
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def get_sub(file_hash, filename="filename.mkv", language="en"):
    logger.info("Downloading subtitles from SubDb")
    logger.debug("Language selected for subtitles: %s" % (language))
    if language.lower() in LANGUAGES:
        r = requests.get(
            DOWNLOAD_URL
            + "&hash="
            + file_hash
            + "&language="
            + language.lower(),
            headers=HEADERS,
        )
        logger.debug(
            "Status code for {} is {}".format(filename, r.status_code)
        )
        if r.status_code == 200:
            with open(os.path.splitext(filename)[0] + ".srt", "wb") as f:
                for chunk in r.iter_content(chunk_size=150):
                    if chunk:
                        f.write(chunk)
            logger.info("Downloaded Subtitles for %s" % (filename))
            return 200
        elif r.status_code == 404:
            logger.info("[SubDB] Subtitle not found for %s" % (filename))
        else:
            logger.debug("Invalid file %s" % (filename))
            print("Invalid file")
    else:
        print("Language not supported")
        return
