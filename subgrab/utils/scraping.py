import logging
import os
import re
import zipfile

import bs4
import requests
from urllib.request import urljoin


logger = logging.getLogger("scraping.py")

def scrape_page(url, parameter=""):
    """
    Retrieve content from a url.
    """
    HEADERS = {
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }

    if parameter:
        req = requests.get(url, params={"query": parameter}, headers=HEADERS)
    else:
        req = requests.get(url, headers=HEADERS)

    if req.status_code != 200:

        logger.error("{} not retrieved.".format(req.url))

    try:
        req_html = bs4.BeautifulSoup(req.content, "lxml")
    except Exception as e:
        logger.error(f"BeautifulSoup not created from {req.content}\n{e}")

    return req_html


def zip_extractor(name):
    """
    Extracts zip file obtained from the Subscene site (which contains subtitles).
    """
    try:
        with zipfile.ZipFile(name, "r") as z:
            # srt += [i for i in ZipFile.namelist() if i.endswith('.srt')][0]
            z.extractall(".")
        os.remove(name)
    except Exception as e:
        logger.warning("Zip Extractor Error: {}".format(e))



def save_subfile(name, new_name=''):
    """
    Save subtitle file to disk.
    """
    if new_name:
        filename = new_name
    else:
        filename = name

    try:
        with open(filename, 'w+') as f:
            f.write(name)
    except Exception as e:
        logger.error(f"Error saving {filename}: {e}")
