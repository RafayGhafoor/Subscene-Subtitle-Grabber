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
        logger.warning("Zip Extractor Error: %s" % (e))

class LanguageNotSupported(IndexError):
    print("Language Not Supported.")


class Subscene(Provider):
    '''Subscene class that is a subclass of Provider (base class) which
    provides functionality for interacting with the subscene site.'''

    LANGUAGES = {'subscene':
                 ('Arabic', 'Burmese','Danish',
                 'Dutch', 'English', 'Farsi_persian',
                 'Indonesian', 'Italian', 'Malay',
                 'Spanish', 'Vietnamese')}


    def __init__(self, base_url, logger_name="Subscene", default_lang="English", mode="prompt"):
        super(Subscene, self).__init__(base_url, default_lang, logger_name)
        self.mode = mode
        self.lang = default_lang
        print(self.lang in self.LANGUAGES['subscene'])
        if self.lang not in self.LANGUAGES['subscene']:
            print("e")
            raise LanguageNotSupported
        self.lang = default_lang


    def silent_mode(self, title_name, category, name=''):
        '''
        An automatic mode for selecting media title from subscene site.
        :param title_name: title names obtained from get_title function.
        '''

        def html_navigator(sort_by="Popular"):
         '''
         Navigates html tree and select title from it. This function is
         called twice. For example, the default (Popular) category for
         searching in is Popular. It will search title first in popular
         category and then in other categories. If default category
         changes, this process is reversed.
         :param category: selects which category should be searched first in
         the html tree.
         '''
         if sort_by == "Popular": # Searches in Popular Category and the categories next to it.
             section = category.find_all_next("div", {"class": "title"})
         else: # Searches in categories above popular tag.
             section = title_name.find_all("div", {"class": "title"})
         for results in section:
             match = 1
             for letter in name.split():
                 if letter.lower() in results.a.text.lower():
                    #  print "NAME: %s, RESULT: %s, MATCH: %s" % (letter, results.a.text, match)
                    # Loops through the name (list) and if all the elements of the
                    # list are present in result, returns the link.
                     if match == len(name.split()):
                         return "https://subscene.com" + results.a.get("href") + "/" + self.lang
                     match += 1

        # Searches first in Popular category, if found, returns the title name
        obt_link = html_navigator(sort_by="Popular")
        if not obt_link:    # If not found in the popular category, searches in other category
            return html_navigator(sort_by="other_than_popular")
        return obt_link


    def cli_mode(self, titles_name, category):
        '''
        A manual mode driven by user, allows user to select subtitles manually
        from the command-line.
        :param titles_name: title names obtained from get_title function.
        '''
        media_titles = [] # Contains key names of titles_and_links dictionary.
        titles_and_links = {} # --> "Doctor Strange" --> "https://subscene.com/.../1345632"

        for i, x in enumerate(category.find_all_next("div", {"class": "title"})):
            title_text = x.text.strip()
            titles_and_links[title_text] = x.a.get("href")
            print("({}): {}".format(i, title_text.encode("ascii", "ignore")))
            media_titles.append(title_text)

        try:
            qs = int(raw_input("\nPlease Enter Movie Number: "))
            return "https://subscene.com" + titles_and_links[media_titles[qs]] + "/" + self.lang

        except Exception as e:
            logger.warning("Movie Skipped - %s" % (e))
            # If pressed Enter, movie is skipped.
            return


    def sel_title(self, name):
        '''
        Select title of the media (i.e., Movie, TV-Series)
        :param title_lst: Title Names from the function get_title
        :param name: Media Name. For Example: "Doctor Strange"
        :param mode: Select CLI Mode or Silent Mode.
        URL EXAMPLE:
        https://subscene.com/subtitles/title?q=Doctor.Strange
        '''
        logger.info("Selecting title for name: %s" % (name))
        if not name:
            print("Invalid Input.")
            return

        soup = self.scrape_page(url=SUB_QUERY, parameter=name)
        logger.info("Searching in query: %s" % (SUB_QUERY + "/?q=" + name))

        try:
            if not soup.find("div", {"class": "byTitle"}):
                # URL EXAMPLE (RETURNED):
                # https://subscene.com/subtitles/release?q=pele.birth.of.the.legend
                logger.info("Searching in release query: %s" % (SUB_QUERY + '?q=' + name.replace(' ', '.')))
                return SUB_QUERY + '?q=' + name.replace(' ', '.')

            elif soup.find("div", {"class": "byTitle"}):
                # for example, if 'abcedesgg' is search-string
                if soup.find('div', {"class": "search-result"}).h2.string == "No results found":
                    print("Sorry, the subtitles for this media file aren't available.")
                    return

        except Exception as e:
            logger.debug("Returning - %s" % (e))
            return

        title_lst = soup.findAll("div", {"class": "search-result"}) # Creates a list of titles
        for titles in title_lst:
            popular = titles.find("h2", {"class": "popular"}) # Searches for the popular tag
            if self.mode == "prompt":
                logger.info("Running in PROMPT mode.")
                return cli_mode(titles, category=popular)
            else:
                logger.info("Running in SILENT mode.")
                return silent_mode(titles, category=popular, name=name.replace('.', ' '))


    # Select Subtitles
    def sel_sub(self, page, sub_count=1, name=""):
        '''
        Select subtitles from the movie page.
        :param sub_count: Number of subtitles to be downloaded.
        URL EXAMPLE:
        https://subscene.com/subtitles/release?q=pele.birth.of.the.legend
        '''
        # start_time = time.time()
        soup = self.scrape_page(page)
        sub_list = []
        current_sub = 0
        for link in soup.find_all('td', {'class': 'a1'}):
            link = link.find('a')
            if current_sub < sub_count and 'trailer' not in link.text.lower()\
                            and link.get('href') not in sub_list and\
                            self.lang in link.text:
                # if movie = Doctor.Strange.2016, this first condition is not
                # going to be executed because the length of the list will be 0
                # we format the name by replacing dots with spaces, which will
                # split it into the length of the list of two elements (0,1,2)
                formatted_name = name.replace('.', ' ').split()
                if name.lower() in link.text.lower():
                    sub_list.append(link.get('href'))
                    current_sub += 1

                if len(name.split()) > 1:
                    if name.split()[1].lower() in link.text.lower() or \
                            name.split()[0].lower() in link.text.lower():
                        sub_list.append(link.get('href'))
                        current_sub += 1

                elif len(formatted_name) > 1:
                    if formatted_name[0].lower() in link.text.lower() or \
                            formatted_name[1].lower() in link.text.lower():
                        sub_list.append(link.get('href'))
                        current_sub += 1

        # print("--- sel_sub took %s seconds ---" % (time.time() - start_time))
        return ['https://subscene.com' + i for i in sub_list]


    def dl_sub(self, page):
        '''
        Download subtitles obtained from the select_subtitle
        function i.e., movie subtitles links.
        '''
        # start_time = time.time()
        soup = self.scrape_page(page)
        div = soup.find('div', {'class': 'download'})
        down_link = 'https://subscene.com' + div.find('a').get('href')
        filename = self.downloader(down_link)
        zip_extractor(filename)
        print("Subtitle (%s) - Downloaded\n" % filename.replace('-', ' ').capitalize())
        # print("--- download_sub took %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    SUB_QUERY = "https://subscene.com/subtitles/release"
    subscene = Subscene(base_url=SUB_QUERY)
