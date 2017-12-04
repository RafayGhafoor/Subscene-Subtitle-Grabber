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


    def get_title(self, page_url):
        '''
        Obtain titles with corresponding links from the subscene page.

        Example of the page from the titles are scraped:-
        >>> https://subscene.com/subtitles/title?q=Doctor.Strange

        Parameters:
        page_url: Page url to get titles from.
        '''
        # No need to scrape page if the base url is directed towards release query
        if page_url.startswith(Subscene.base_url_release):
            return
        # name of the titles:
        titles = [] # "Person of interest Fifth Season"
        # links to subtitles page:
        sub_links = []  # "/subtitles/person-of-interest-season-5"
        soup = self.scrape_page(page_url)
        page = soup.findAll("div", class_="title") # Titles menu

        for links in page:
            # The subscene titles page include titles in three categories i.e,
            # Popular, Exact, TV-Series (We ignore the close category).
            if links.a.get('href') not in sub_links:
                # A check to filter duplicate urls of the same name since they
                # are scattered in different categories.
                titles.append(links.text.strip())
                sub_links.append(links.a.get('href'))

        return (titles, sub_links)
