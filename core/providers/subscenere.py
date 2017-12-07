import requests
import re
import bs4
import zipfile
import os
import logging
from provider import Provider

def zip_extractor(name):
    '''
    Extracts zip file obtained from the Subscene site (which contains subtitles).
    '''
    try:
        with zipfile.ZipFile(name, "r") as z:
            # srt += [i for i in ZipFile.namelist() if i.endswith('.srt')][0]
            z.extractall(".")
        os.remove(name)
    except Exception as e:
        self.logger.warning("Zip Extractor Error: %s" % (e))


class LanguageNotSupported(Exception):
    def __init__(self, language):
        self.language = language
        super(LanguageNotSupported, self).__init__(self, '{} is not supported by the provider.'.format(language))


class Subscene(Provider):
    '''Subscene class that is a subclass of Provider (base class) which
    provides functionality for interacting with the subscene site.'''

    base_url_release = "https://subscene.com/subtitles/release/?q="
    base_url_title = "https://subscene.com/subtitles/title?q="
    # To Force searching in release page add, &r=true as a parameter in
    # base_url_release

    def __init__(self, logger_name="Subscene", lang="English"):
        super(Subscene, self).__init__(lang, logger_name)
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
        print("Subtitle (%s) - Downloaded\n" % filename.replace('-', ' ').capitalize())
        return filename
