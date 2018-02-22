import os.path
import hashlib

import requests

from provider import Provider, LanguageNotSupported

HEADERS = {'User-agent': "SubDB/1.0 (subgrab/1.0; http://github.com/RafayGhafoor/Subscene-Subtitle-Grabber)"}

# Provider agnostic exception

class InvalidFile(Exception):
    def __init__(self, filename):
        self.file = filename
        super(InvalidFile, self).__init__(self, '{} is a invalid file.'.format(self.file))


class SubDB(Provider):

    def __init__(self, lang="en"):
        super(SubDB, self).__init__(lang)
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


    def get_sub(self, filename):
        r = requests.get(self.DOWNLOAD_URL + '&hash=' + self.get_hash(filename) + '&language=' + self.lang, headers=HEADERS)

        if r.status_code == 404:
            #TODO: Write log message.
            pass
        elif r.status_code == 200:
            with open(os.path.splitext(filename)[0] + '.srt', 'wb') as f:
                for chunk in r.iter_content(chunk_size=150):
                    if chunk:
                        f.write(chunk)
        else:
            #TODO: raise exception.
            raise InvalidFile
