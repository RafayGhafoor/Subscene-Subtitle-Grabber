import logging
import os.path
import hashlib
import requests
from provider import Provider, LanguageNotSupported

HEADERS = {'User-agent': "SubDB/1.0 (subgrab/1.0; http://github.com/RafayGhafoor/Subscene-Subtitle-Grabber)"}

class SubDB(Provider):
    def __init__(self, logger_name="SubDB", lang="en"):
        super(SubDB, self).__init__(lang, logger_name)
        self.lang = lang
        self.provider_lang = self.get_lang('allsubdb')
        if self.lang not in self.provider_lang:
            raise LanguageNotSupported(lang)
        self.lang = lang
        self.DOWNLOAD_URL = "http://api.thesubdb.com/?action=download"

    def get_hash(self, filename):
        readsize = 64 * 1024
        with open(filename, 'rb') as f:
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

    def get_sub(self, filename, language='en'):
        self.logger.info("Downloading subtitles from SubDB")
        self.logger.debug("Language selected for subtitles: %s" % (language))
        r = requests.get(self.DOWNLOAD_URL + '&hash=' + self.get_hash(filename) + '&language=' + self.lang, headers=HEADERS)
        self.logger.debug("Status code for %s is %s" % (filename, r.status_code))

        if r.status_code == 404:
            self.logger.info("[SubDB] Subtitle not found for %s" % (filename))

        elif r.status_code == 200:
            with open(os.path.splitext(filename)[0] + '.srt', 'wb') as f:
                for chunk in r.iter_content(chunk_size=150):
                    if chunk:
                        f.write(chunk)
            self.logger.info("Downloaded Subtitles for %s" % (filename))
            return 200

        else:
            self.logger.debug("Invalid file %s" % (filename))
            print("Invalid file")
