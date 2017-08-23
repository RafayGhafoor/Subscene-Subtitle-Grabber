import time
import requests
import re
import timeit
import bs4
import zipfile
import os
os.chdir("N:\Rafay\Anime\Anime Movies")
SUB_QUERY = "https://subscene.com/subtitles/release"
LANGUAGE = {
"AR" : "Arabic",
"BU" : "Burmese",
"DA" : "Danish",
"DU" : "Dutch",
"EN" : "English",
"FA" : "Farsi_persian",
"IN" : "Indonesian",
"IT" : "Italian",
"MA" : "Malay",
"SP" : "Spanish",
"VI" : "Vietnamese"
}

DEFAULT_LANG = LANGUAGE["EN"]


def scrape_page(url, parameter=''):
    '''Allows you to get content from a url.'''
    if parameter:
        req = requests.get(url, params={'q': parameter})
    else:
        req = requests.get(url)
    # print 'Generated URL is ---> %r\n' % req.url
    req_html = bs4.BeautifulSoup(req.content, "lxml")
    return req_html


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
        pass


def silent_mode(title_name, name='', year=''):
    '''
    An automatic mode for selecting media title from subscene site.
    :param title_name: title names obtained from get_title function.
    '''
    def html_navigator(category="Popular"):
     '''
     Navigates html tree and select title from it. This function is
     called twice. For example, the default (Popular) category for
     searching in is Popular. It will search title first in popular
     category and then in other categories. If default category
     changes, this process is reversed.
     :param category: selects which category should be searched first in
     the html tree.
     '''
     popular = title_name.find("h2", {"class": "popular"})
     if category == "Popular": # Searches in Popular Category and the categories next to it.
         section = popular.find_all_next("div", {"class": "title"})
     else: # Searches in categories above popular tag.
         section = title_name.find_all("div", {"class": "title"})
     for results in section:
         match = 1
         for letter in name.split():
             if letter.lower() in results.a.text.lower() and year in results.a.text.lower():
                 if len(name.split()) == match:
                     return "https://subscene.com" + results.a.get("href") + "/" + DEFAULT_LANG
                 match += 1

    # Searches first in Popular category, if found, returns the title name
    obt_link = html_navigator(category="Popular")
    if not obt_link:    # If not found in the popular category, searches in other category
     return html_navigator(category="other_than_popular")
    return obt_link


def cli_mode(titles_name):
    '''
    A manual mode driven by user, allows user to select subtitles manually
    from the command-line.
    :param titles_name: title names obtained from get_title function.
    '''
    media_titles = [] # Contains key names of titles_and_links dictionary.
    titles_and_links = {} # --> "Doctor Strange" --> "https://subscene.com/.../1345632"
    popular = titles_name.find("h2", {"class": "popular"})

    for i, x in enumerate(popular.find_all_next("div", {"class": "title"})):
        title_text = x.text.strip()
        titles_and_links[title_text] = x.a.get("href")
        print "(%s): %s" % (i, title_text.encode("ascii", "ignore"))
        media_titles.append(title_text)

    qs = int(raw_input("\nPlease Enter Movie Number: "))
    return "https://subscene.com" + titles_and_links[media_titles[qs]] + "/" + DEFAULT_LANG


def select_title(name='', year='', mode="prompt"):
    '''
    Select title of the media (i.e., Movie, TV-Series)
    :param title_lst: Title Names from the function get_title
    :param name: Media Name. For Example: "Doctor Strange"
    :param year: Media Year. For Example: "2016"
    :param mode: Select CLI Mode or Silent Mode.
    '''
    if not name and not year:
        print "Invalid Input."
        return

    soup = scrape_page(url=SUB_QUERY, parameter=name)
    try:
        if soup.find("div", {"class": "byTitle"}):
            if soup.find('div', {"class": "search-result"}).h2.string == "No results found":
                print "Sorry, the subtitles for this media file aren't available."
                return

        elif not soup.find("div", {"class": "byTitle"}):
            return SUB_QUERY + '?q=' + name.replace(' ', '.')

    except AttributeError:
        # print name, year
        return

    title_lst = soup.findAll("div", {"class": "search-result"})
    for titles in title_lst:
        popular = titles.find("h2", {"class": "popular"}) # Searches for the popular tag
        if mode == "prompt":
            return cli_mode(titles)
        else:
            silent_mode(titles)


# Select Subtitles
def sel_sub(page, sub_count=1, name=""):
    '''
    Select subtitles from the movie page.
    :param sub_count: Number of subtitles to be downloaded.
    '''
    # start_time = time.time()
    soup = scrape_page(page)
    sub_list = []
    active_sub = 0
    for link in soup.find_all('td', {'class': 'a1'}):
        link = link.find('a')
        if active_sub < sub_count and 'Trailer' not in link.text\
                        and link.get('href') not in sub_list and\
                        DEFAULT_LANG in link.text:
            if len(name.split()) > 1:
                if name.split()[1].lower() in link.text.lower() or \
                                    name.split()[0].lower() in link.text.lower():
                    sub_list.append(link.get('href'))
                    active_sub += 1
            else:
                sub_list.append(link.get('href'))
                active_sub += 1
    # print("--- sel_sub took %s seconds ---" % (time.time() - start_time))
    return ['https://subscene.com' + i for i in sub_list]


def dl_sub(page):
    '''
    Download subtitles obtained from the select_subtitle
    function i.e., movie subtitles links.
    '''
    # start_time = time.time()
    srt = ""
    soup = scrape_page(page)
    div = soup.find('div', {'class': 'download'})
    down_link = 'https://subscene.com' + div.find('a').get('href')
    r = requests.get(down_link, stream=True)
    fname = re.findall("filename=(.+)", r.headers['content-disposition'])  # File Name
    for found_sub in fname:
        name = found_sub.replace('-', ' ')
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=150):
                if chunk:
                    f.write(chunk)
        zip_extractor(name)
    print "Subtitle (%s) - Downloaded" % name.capitalize()
    # print("--- download_sub took %s seconds ---" % (time.time() - start_time))
