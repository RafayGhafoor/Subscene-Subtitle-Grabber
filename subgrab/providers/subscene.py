import logging
import os
import re
import zipfile

import bs4
import requests


logger = logging.getLogger("subscene.py")
SUB_QUERY = "https://subscene.com/subtitles/searchbytitle"
LANGUAGE = {
    "AR": "Arabic",
    "BU": "Burmese",
    "DA": "Danish",
    "DU": "Dutch",
    "EN": "English",
    "FA": "Farsi_persian",
    "IN": "Indonesian",
    "IT": "Italian",
    "MA": "Malay",
    "SP": "Spanish",
    "VI": "Vietnamese",
}
MODE = "prompt"
DEFAULT_LANG = LANGUAGE["EN"]  # Default language in which subtitles
# are downloaded.


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
        logger.debug("{} not retrieved.".format(req.url))
        return
    req_html = bs4.BeautifulSoup(req.content, "lxml")
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
        if (
            sort_by == "Popular"
        ):  # Searches in Popular Category and the categories next to it.
            section = category.find_all_next("div", {"class": "title"})
        else:  # Searches in categories above popular tag.
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
            and DEFAULT_LANG in link.text
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
