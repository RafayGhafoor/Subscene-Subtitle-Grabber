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
        # No need to scrape page if the base url is directed towards release query
        if page_url.startswith(Subscene.base_url_release):
            return

        menu = {} # --> "Doctor Strange" --> "https://subscene.com/.../1345632"
        soup = self.scrape_page(page_url)
        page = soup.findAll("div", {"class": "search-result"}) # Titles menu
        for titles in page:
            exact = titles.find("h2", {"class": "exact"}) # Searches in the exact tag
            popular = titles.find("h2", {"class": "popular"}) # Searches in the popular tag
            # for x in popular.find_all_next("div", {"class": "title"}):
            #     title_text = x.text.strip()
            #     titles_and_links[title_text] = x.a.get("href")


if __name__ == '__main__':
    subscene = Subscene()
    subscene.get_title("https://subscene.com/subtitles/title?q=person+of+interest&l=")
    # sub_link = subscene.sel_title(name="Doctor Strange")
    # if sub_link:
    #     for i in subscene.sel_sub(page=sub_link, name="Doctor Strange"):
    #         subscene.dl_sub(i)
