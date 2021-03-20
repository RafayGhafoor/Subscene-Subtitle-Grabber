import logging
import os
import re
import zipfile
import pickle

import bs4
import requests
from collections import defaultdict
from urllib.request import urljoin
from subgrab.utils.scraping import scrape_page
from subgrab.utils.scraping import zip_extractor
from subgrab.utils.titleparser import parse_title

# DEBUGGINg with iPython
from IPython import embed

logger = logging.getLogger("addic7ed.py")

SUB_QUERY = "https://www.addic7ed.com/search.php?search="
#MODE = "prompt"

def search(parameter='', lang='', count=''):
    """
    Show search results and provide selection of one entry.
    """

    soup = scrape_page(url=f"{SUB_QUERY}{' '.join(parameter)}")
    titles = soup.select('table[class^=tabel] a')
    title_dict = _get_data(titles, lang=lang)
    selected = select_title(title_dict)

    for sel in selected:
        sel_soup = dl_sub(sel['url'], '.buttonDownload')

def _get_data(bs4elementTagList, **kwargs):
    """
    Get data about subtitles.
    """
    try:
        lang = kwargs['lang']
    except KeyError as e:
        print(f"Language not in language dict.\n{e}")


    def get_dl_urls(url):
        """
        Returns download urls.
        """
        pass

    title_dict = defaultdict(list)

    for bs4elementTag in bs4elementTagList:

        # title
        title = bs4elementTag.text.strip()
        logger.debug(f"TITLE: {title}")

        # url (language specific) by replacing last part by LANGUAGE
        url_rel = bs4elementTag['href']

        # series data: ser_title, ser_no, ep_no, ep_title, name
        if url_rel.startswith('serie'):
            url = urljoin('https://addic7ed.com',
                      re.sub(r'[^/]+$', f'{lang}', url_rel))
            ser_data = {**parse_title(title), 'serie': True}
            # create new title for the defaultdict key (1 Series)
            title = f"{ser_data['ser_title']} - Season {ser_data['ser_no']}"
        else:
            ser_data = {'serie': False}
            url = urljoin('https://addic7ed.com', url_rel)

        logger.debug(f"URL: {url}")

        # set title as keys to fill defaultdict
        title_dict[title].append({'url': url, 'title': title, **ser_data})

    print(title_dict)
    #_pickle('title_dict.pickle', title_dict)
    return title_dict

    #yeah

def select_title(titles_dict, col_width=int(60) ):
    """
    Print available titles for selection and returns a list of
    episodes/movie data (as dictionary).

    series episodes and movies:

    url: url to crawl subtitles from

    series episodes:

    title:     <ser_title> - Season <ser_no> (concatenated string)
    ser_title: series title
    ser_no:    series number (2-digits)
    ep_title:  episode title
    ep_no:     episode number (2-digits)
    name:      suggested name for renaming (without extension):
               <ser_title> - S<ser_no>E<ep_no> - <ep_title>
    serie:     True (boolean) to identify as serie

    movies:

    title:     movie title
    serie:     False (boolean) to identify as movie
    """
    # exchange keys to with selection number
    select_dict = {}
    i = 0

    for title, data in titles_dict.items():

        select_dict[i] = data
        i += 1

    # seperate selection list
    print('\n')

    for i, data in select_dict.items():

        # pretty print results for selection
        width = len(f"({i}): {data[0]['title']}")

        # short entries: pretty print
        if width < col_width:

            fill = col_width - width
            if data[0]['serie']:
                type = 'Serie'
            else:
                type = 'Movie'

            print(f"({i}): {data[0]['title']}{' '*fill}| {type}")

        # long entries: print as short as possible
        else:

            print(f"({i}): {data[0]['title']} | {type}")

    try:
        qs = int(input("\nPlease Enter Movie Number: "))

        if qs in select_dict.keys():

            print(f"{select_dict[qs]}")
            return select_dict[qs]

        else:
            logger.error("Movie number is not valid.")


    except Exception as e:
        logger.warning("Movie Skipped - {}".format(e))
        # If pressed Enter, movie is skipped.
        return

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
def _pickle(filename, object):
    "Pickle object and save to current directory."
    with open(filename, 'wb') as f:
        pickle.dump(object, f)
