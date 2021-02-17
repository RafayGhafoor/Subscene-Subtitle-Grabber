import logging
import os
import re
import zipfile

import bs4
import requests
from collections import defaultdict
from urllib.request import urljoin
from subgrab.utils.scraping import scrape_page
from subgrab.utils.scraping import zip_extractor

logger = logging.getLogger("addic7ed.py")

SUB_QUERY = "https://www.addic7ed.com/search.php?search="
#MODE = "prompt"

def get_data(bs4elementTag):
    """
    Get data about subtitles

        - title
        - URL
        - debug value

    remember: A bs4.element.ResultSet which will be returned by select method
              are list objects. Get the element.Tag by using the index [0].
    """
    sub_title_links = {}

    logger.debug(f"bs4.element.Tag: {bs4elementTag}")

    title = bs4elementTag.text.strip()
    logger.debug(f"TITLE: {title}")
    # replacing the last part by language No does the job
    url = urljoin('https://addic7ed.com',
                  re.sub(r'[^/]+$', f'{LANG}', bs4elementTag['href']))
    logger.debug(f"URL: {url}")
    # note: debug value us used as id in following url,
    # but this could not directly acessed (without the
    # correct right referer, cookies etc.):
    # https://www.addic7ed.com/original/157750/1
    #                                  |--ID--| No. 0 ... z
    debug = bs4elementTag['debug']
    logger.debug(f"DEBUG: {debug}")

    sub_title_links = {'title': title,
                       'url': url,
                       'debug': debug}

    print(sub_title_links)
    return sub_title_links


def dl_sub(page, css_selector):
    """
    Download subtitles obtained from the select_subtitle
    function i.e., movie subtitles links.
    """
    headers = {
        'authority':     'www.addic7ed.com',
        #'method':     'GET',
        #'path':     '/original/157750/1',
        #'scheme':     'https',
        #'accept':     'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #'accept-encoding':     'gzip, deflate, br',
        #'accept-language':     'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        #'cookie':     'PHPSESSID=fegtfsdrdlhdl4sml8pb9s6314',
        #'dnt': '1',
        'referer': 'https://www.addic7ed.com/serie/Bless%20This%20Mess/2/20/addic7ed',
        #'sec-fetch-dest':     'document',
        #'sec-fetch-mode':     'navigate',
        #'sec-fetch-site ':    'same-origin',
        #'sec-fetch-user':     '?1',
        #'upgrade-insecure-requests':     '1',
        'user-agent':     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.142 Safari/537.36'
    }
    # start_time = time.time()
    soup = scrape_page(page)
    elements = soup.select(css_selector)
    for elem in elements:
        down_link = urljoin(SUB_QUERY, elem['href'])
        print(down_link)
    r = requests.get(down_link, headers=headers, stream=True)
    for found_sub in re.findall(
        "filename=(.+)", r.headers["content-disposition"]
    ):
        with open(found_sub.replace("-", " "), "wb") as f:
            for chunk in r.iter_content(chunk_size=150):
                if chunk:
                    f.write(chunk)
        #zip_extractor(found_sub.replace("-", " "))
    print(
        "Subtitle ({}) - Downloaded\n".format(
            found_sub.replace("-", " ").capitalize()
        )
    )

        # print("--- download_sub took %s seconds ---" % (time.time() - start_time))
