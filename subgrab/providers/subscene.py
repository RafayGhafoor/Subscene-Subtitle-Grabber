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

# DEBUGGINg with iPython
from IPython import embed

logger = logging.getLogger("subscene.py")

SUB_QUERY = "https://subscene.com/subtitles/searchbytitle"
MODE = "prompt"

def search(parameter='', lang='', count=''):
    """
    Show search results and provide selection of one entry.
    """
    soup = scrape_page(url=SUB_QUERY,
                       parameter=parameter)

    titles_dict = search_titles(soup)

    if not titles_dict:

        print("No entry found.")

    else:

        title_url = select_title(titles_dict, lang)

        soup = scrape_page(url=title_url)

        entries_dict = get_entries(soup)
        print(entries_dict)

        # safe to json (to not have to crawl again)
        target = Path('.').joinpath('subtitles.json')
        if not target.exists():
            with open(target, 'w+') as f:
                json.dump(dict(entries_dict), f)

        entries_urls = PROVIDER.get_dl_pages(entries_dict, count)

        embed()

        for url in entries_urls:

            dl_sub(url)


def search_titles(soup, category='all'):
    """
    Returns a dict with numbers starting from 0 as keys and a dictionary
    as value, where the keys are:

        title: title of the movie/series
        url: url to the subtitles for that title
        count: no of available subtitles for that title

    The results are put into categories by subscene:

        exact: exact match
        series: TV-Series matches
        close: close matches
        popular: popular matches

    TODO: describe te rest...
    """

    # check for any result
    if not soup.select('h2 ~ ul'):

        print("Sorry, the subtitles for this media file aren't available.")

    else:

        # dict & counter (to generate the keys)
        titles_dict = {}
        i = 0

        if 'all' in category:

            # select all results and skip further categories
            selectors = soup.select('h2 ~ ul > li')
            for selector in selectors:
                titles_dict[i] = get_data(selector)
                logger.debug(f"Dict entry with key={i} successlly written.")
                i += 1

        else:

            if 'popular' in category:

                selectors = soup.select('h2.popular ~ ul > li')
                for selector in selectors:
                    titles_dict[i] = get_data(selector)
                    i += 1

            if 'exact' in category:

                selectors = soup.select('h2.exact ~ ul > li')
                for selector in selectors:
                    titles_dict[i] = get_data(selector)
                    i += 1

            if 'series' in category:

                selectors = soup.select('h2:contains("TV-Series") ~ ul > li')
                for selector in selectors:
                    titles_dict[i] = get_data(selector)
                    i += 1

            if 'close' in category:

                selectors = soup.select('h2.close ~ ul > li')
                for selector in selectors:
                    titles_dict[i] = get_data(selector)
                    i += 1

        return titles_dict


def select_title(titles_dict, LANGUAGE, col_width=int(60) ):
    """
    Returns the url to all subtitles of the selected title and language.
    Available titles are printed for selection.
    """
    lang = LANGUAGE

    # seperate selection list
    print('\n')

    for i, data in titles_dict.items():

        # pretty print results for selection
        width = len(f"({i}): {data['title']}")

        if width < col_width:

            fill = col_width - width
            print(f"({i}): {data['title']}{' '*fill}| {data['count']} (all languages)")

        else:

            print(f"({i}): {data['title']} | {data['count']}")

    try:
        qs = int(input("\nPlease Enter Movie Number: "))

        if qs in titles_dict.keys():

            print(f"{titles_dict[qs]['url']}/{lang['name']}")
            return f"{titles_dict[qs]['url']}/{lang['name']}"

        # test im Browser:
        # https://subscene.com/
        # https://subscene.com/subtitles/bless-this-mess-second-season/en
        # or
        # https://subscene.com/subtitles/bless-this-mess-second-season/13
        # ITS THE NAME OF THE LANGUAGE!

        else:
            logger.error("Movie number is not valid.")


    except Exception as e:
        logger.warning("Movie Skipped - {}".format(e))
        # If pressed Enter, movie is skipped.
        return


def get_data(bs4elementTag):
    """
    Get data about subtitles:

        - title
        - URL
        - subtitle count

    remember: A bs4.element.ResultSet which will be returned by select method
              are list objects. Get the element.Tag by using the index [0].
    """

    sub_title_links = {}

    logger.debug(f"bs4.element.Tag: {bs4elementTag}")

    title = bs4elementTag.select_one('a').text
    logger.debug(f"TITLE: {title}")
    url = urljoin('https://subscene.com', bs4elementTag.select_one('a')['href'])
    logger.debug(f"URL: {url}")
    count = bs4elementTag.select_one('.count').text.strip()
    logger.debug(f"COUNT: {count}")

    sub_title_links = {'title': title, 'url': url, 'count': count}

    return sub_title_links


def get_entries(soup):
    """
    Returns a dictionary with episode numbers (e.g. S01E01) as keys and
    a list of urls to the final pages, where the subtitles can be
    downloaded, as values.

    """
    results = soup.select('tbody > tr')

    subs = defaultdict(list)
    # note: some links will be duplicates, butset prevent the dict to
    # save as json. set should be created directly before downloading

    for r in results:

        if r.select_one('td[class="banner-inlist"]'):

            # skip banner rows
            continue

        else:

            try:

                filename = r.select_one('span:nth-child(2)').text.strip()
                url = urljoin('https://subscene.com', r.select_one('a')['href'])
                episode = re.search(r'S\d+E\d+', filename).group()
                #info = r.select_one('div').text.strip()
                #duration = re.search(r'(\d+:\d+)', info).group()
                #source = re.search(r'From\s([a-zA-Z0-7.]+)', info).group(1)
                print(f"filename: {filename}")
                print(f"URL:      {url}")
                print(f"episode:  {episode}")
                #print(f"duration: {duration}")
                #print(f"source:   {source}\n")

                subs[episode].append(url)

            except AttributeError:

                # no subtitle for given language: pass silently
                pass

    if not subs:

        logger.info("No subtitle available for given language.")

    else:

        return subs


def get_dl_pages(entries_dict, max_files):
    """
    Returns as iterator with urls limited by max_files argument.
    These urls can be delived to the dl_sub function.
    """
    links = []

    for _, urls in entries_dict.items():

        for url in list(set(urls))[:max_files]:

            links.append(url)

    return links


def silent_mode(title_name, category, name=""):
    """
    An automatic mode for selecting media title from subscene site.
    :param title_name: title names obtained from get_title function.
    """

    def html_navigator(sort_by="Popular"):
        """
     Navigates html tree and select title from it. This function is
     called twice. For example, the default (Popular) category for
     searching in is Popular. It will search title first in popular
     category and then in other categories. If default category
     changes, this process is reversed.
     :param category: selects which category should be searched first in
     the html tree.
     """
        # Searches in Popular Category and the categories next to it.
        if sort_by == "Popular":
            section = category.find_all_next("div", {"class": "title"})
        # Searches in categories above popular tag.
        else:
            section = title_name.find_all("div", {"class": "title"})
        for results in section:
            match = 1
            for letter in name.split():
                if letter.lower() in results.a.text.lower():
                    #  print "NAME: %s, RESULT: %s, MATCH: %s" % (letter, results.a.text, match)
                    # Loops through the name (list) and if all the elements of the
                    # list are present in result, returns the link.
                    if match == len(name.split()):
                        return (
                            "https://subscene.com"
                            + results.a.get("href")
                            + "/"
                            + DEFAULT_LANG
                        )
                    match += 1

    # Searches first in Popular category, if found, returns the title name
    obt_link = html_navigator(sort_by="Popular")
    if (
        not obt_link
    ):  # If not found in the popular category, searches in other category
        return html_navigator(sort_by="other_than_popular")
    return obt_link


def cli_mode(titles_name, category):
    """
    A manual mode driven by user, allows user to select subtitles manually
    from the command-line.
    :param titles_name: title names obtained from get_title function.
    """
    media_titles = []  # Contains key names of titles_and_links dictionary.
    titles_and_links = (
        {}
    )  # --> "Doctor Strange" --> "https://subscene.com/.../1345632"
    for i, x in enumerate(category.find_all_next("div", {"class": "title"})):
        title_text = x.text.encode("ascii", "ignore").decode("utf-8").strip()
        titles_and_links[title_text] = x.a.get("href")
        print("({}): {}".format(i, title_text))
        media_titles.append(title_text)

    try:
        qs = int(input("\nPlease Enter Movie Number: "))
        return (
            "https://subscene.com"
            + titles_and_links[media_titles[qs]]
            + "/"
            + DEFAULT_LANG
        )

    except Exception as e:
        logger.warning("Movie Skipped - {}".format(e))
        # If pressed Enter, movie is skipped.
        return


def sel_title(name):
    """
    Select title of the media (i.e., Movie, TV-Series)
    :param title_lst: Title Names from the function get_title
    :param name: Media Name. For Example: "Doctor Strange"
    :param mode: Select CLI Mode or Silent Mode.
    URL EXAMPLE:
    https://subscene.com/subtitles/title?query=Doctor.Strange
    """
    logger.info("Selecting title for name: {}".format(name))
    if not name:
        print("Invalid Input.")
        return

    soup = scrape_page(url=SUB_QUERY, parameter=name)
    logger.info("Searching in query: {}".format(SUB_QUERY + "/?query=" + name))
    try:
        if not soup.find("div", {"class": "byTitle"}):
            # URL EXAMPLE (RETURNED):
            # https://subscene.com/subtitles/searchbytitle?query=pele.birth.of.the.legend
            logger.info(
                "Searching in release query: {}".format(
                    SUB_QUERY + "?query=" + name.replace(" ", ".")
                )
            )
            return SUB_QUERY + "?query=" + name.replace(" ", ".")

        elif soup.find("div", {"class": "byTitle"}):
            # for example, if 'abcedesgg' is search-string
            if (
                soup.find("div", {"class": "search-result"}).h2.string
                == "No results found"
            ):
                print(
                    "Sorry, the subtitles for this media file aren't available."
                )
                return

    except Exception as e:
        logger.debug("Returning - {}".format(e))
        return

    title_lst = soup.findAll(
        "div", {"class": "search-result"}
    )  # Creates a list of titles
    for titles in title_lst:
        popular = titles.find(
            "h2", {"class": "popular"}
        )  # Searches for the popular tag
        if MODE == "prompt":
            logger.info("Running in PROMPT mode.")
            return cli_mode(titles, category=popular)
        else:
            logger.info("Running in SILENT mode.")
            return silent_mode(
                titles, category=popular, name=name.replace(".", " ")
            )


# Select Subtitles
def sel_sub(page, sub_count=1, name=""):
    """
    Select subtitles from the movie page.
    :param sub_count: Number of subtitles to be downloaded.
    URL EXAMPLE:
    https://subscene.com/subtitles/searchbytitle?query=pele.birth.of.the.legend
    """
    # start_time = time.time()
    soup = scrape_page(page)
    sub_list = []
    current_sub = 0
    for link in soup.find_all("td", {"class": "a1"}):
        link = link.find("a")
        if (
            current_sub < sub_count
            and "trailer" not in link.text.lower()
            and link.get("href") not in sub_list
            and DEFAULT_LANG.lower() in link.get("href")
        ):
            # if movie = Doctor.Strange.2016, this first condition is not
            # going to be executed because the length of the list will be 0
            # we format the name by replacing dots with spaces, which will
            # split it into the length of the list of two elements (0,1,2)
            formatted_name = name.replace(".", " ").split()
            if name.lower() in link.text.lower():
                sub_list.append(link.get("href"))
                current_sub += 1

            if len(name.split()) > 1:
                if (
                    name.split()[1].lower() in link.text.lower()
                    or name.split()[0].lower() in link.text.lower()
                ):
                    sub_list.append(link.get("href"))
                    current_sub += 1

            elif len(formatted_name) > 1:
                if (
                    formatted_name[0].lower() in link.text.lower()
                    or formatted_name[1].lower() in link.text.lower()
                ):
                    sub_list.append(link.get("href"))
                    current_sub += 1

    # print("--- sel_sub took %s seconds ---" % (time.time() - start_time))
    return ["https://subscene.com" + i for i in sub_list]


def dl_sub(page):
    """
    Download subtitles obtained from the select_subtitle
    function i.e., movie subtitles links.
    """
    # start_time = time.time()
    soup = scrape_page(page)
    div = soup.find("div", {"class": "download"})
    down_link = "https://subscene.com" + div.find("a").get("href")
    r = requests.get(down_link, stream=True)
    for found_sub in re.findall(
        "filename=(.+)", r.headers["content-disposition"]
    ):
        with open(found_sub.replace("-", " "), "wb") as f:
            for chunk in r.iter_content(chunk_size=150):
                if chunk:
                    f.write(chunk)
        zip_extractor(found_sub.replace("-", " "))
    print(
        "Subtitle ({}) - Downloaded\n".format(
            found_sub.replace("-", " ").capitalize()
        )
    )
    # print("--- download_sub took %s seconds ---" % (time.time() - start_time))
