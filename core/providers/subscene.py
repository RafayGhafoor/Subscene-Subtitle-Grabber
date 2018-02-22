'''A minimal API for subscene site.'''
import re
import zipfile
import os

import requests
import bs4

from provider import Provider, LanguageNotSupported


def zip_extractor(name):
    '''Extract zip file obtained from the subscene site.'''
    try:
        with zipfile.ZipFile(name, "r") as z:
            z.extractall(".")
        os.remove(name)
    except Exception as e:
        # TODO: Write log message.
        pass


class Subscene(Provider):
    '''Subscene class that is a subclass of Provider (base class) which
    provides functionality for interacting with the subscene site.'''

    base_url_release = "https://subscene.com/subtitles/release/?q="
    base_url_title = "https://subscene.com/subtitles/title?q="
    # To force searching in release page add, &r=true as a parameter in
    # base_url_release (var)

    def __init__(self, lang="English"):
        super(Subscene, self).__init__(lang)
        self.lang = lang
        self.provider_lang = self.get_lang('subscene')

        if self.lang not in self.provider_lang:
            raise LanguageNotSupported(lang)

        self.lang = lang


    def get_title(self, name):
        '''
        Obtain titles with corresponding links from the subscene page.

        Example of the page from the titles are scraped:-
        >>> https://subscene.com/subtitles/title?q=Doctor.Strange

        Parameters:
        page_url: Page url to get titles from.
        '''
        # No need to scrape page if the base url is directed towards release query
        page_url = self.url_format(base_url=Subscene.base_url_title, query=name)

        if page_url.startswith(Subscene.base_url_release):
            return

        menu = {} # name of the titles and their corresponding links.
        soup = self.scrape_page(page_url)
        page = soup.findAll("div", class_="title") # Titles menu

        for links in page:
            # The subscene titles page include titles in three categories i.e,
            # Popular, Exact, TV-Series (We ignore the close category).
            if links.a.get('href') not in menu:
                # A check to filter duplicate urls of the same name since they
                # are scattered in different categories.
                menu[links.text.strip()] = "https://subscene.com" + links.a.get('href')

        return menu


    def get_sub(self, page_url, sub_count='n'):
        '''
        Obtain subtitles from the release page.

        Example of the page from the titles are scraped:-
        >>> https://subscene.com/subtitles/doctor-strange-2016

        Parameters:
        page_url: link to scrap subtitles from.
        '''
        soup = self.scrape_page(page_url)
        release_info = {}   # Titles and URLS
        current_sub = 0

        for link in soup.find_all('td', class_='a1'):
            if sub_count != 'n' and current_sub == sub_count:
                break

            contents = link.contents[1]
            cleanize = lambda s: s.text.lower().strip()
            url = "https://subscene.com" + contents.get('href')
            release_lang = cleanize(contents.span)
            title = cleanize(contents.span.find_next_sibling("span"))

            if 'trailer' not in title and self.lang.lower() in release_lang:
                if url not in release_info and title not in release_info.values():
                    release_info[url] = title
                    current_sub += 1

        return release_info


    def dl_sub(self, page):
        '''
        Downloads subtitles for the media file.
        '''
        soup = self.scrape_page(page)
        div = soup.find('div', class_='download')
        down_link = 'https://subscene.com' + div.find('a').get('href')
        filename = self.downloader(down_link)
        zip_extractor(filename)

        return filename
