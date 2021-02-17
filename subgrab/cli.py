import argparse
import logging
import logging.config  # not needed I guess, import logging do it
import os
import sys
import json
from pathlib import Path

from subgrab.providers import subscene
from subgrab.providers import subdb
from subgrab.providers import addic7ed
from subgrab.utils import directory
from subgrab.utils.languages import get_languages
from subgrab.utils.scraping import scrape_page


PROVIDERS = ['subscene',
             'subdb',
             'addic7ed']

# LOG CONFIGURATION
if os.sep == "\\":
    # Windows OS
    log_home = Path.home().joinpath("AppData", "Local")
else:
    # Other than Windows
    if not os.getenv("XDG_DATA_HOME"):
        log_home = os.getenv("XDG_DATA_HOME",
                             default=Path.home().joinpath(".local", "share"))

log_directory = log_home.joinpath("Subgrab")

if not log_directory.exists():
    log_directory.mkdir()

logfile_name = log_directory.joinpath("subgrab.log")

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "standard",
            "filename": logfile_name,
        },
    },
    "loggers": {
        "SubGrab": {"handlers": ["file"], "level": "INFO", "propagate": True},
        "directory": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "subscene": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger("SubGrab")

# MAIN FUNCTION
def main():

    # CLI DEFINITION
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dir",
                        default=".",
                        help="Specify directory to work in.")
    parser.add_argument("-m", "--media-name",
                        nargs="*",
                        metavar='media_name',
                        help="Provide movie name.")
    parser.add_argument("-p", "--provider",
                        choices=PROVIDERS,
                        default='subscene')
    parser.add_argument("-s", "--silent",
                        action="store_true",
                        help="Silent mode.")
    parser.add_argument("-c", "--count",
                        type=int,
                        default=1,
                        help="Number of subtitles to be downloaded.")
    parser.add_argument("-l", "--lang",
                        default="EN",
                        help="Change language.")
    parser.add_argument("-deb", "--debug",
                        type=str,
                        default="info",
                        help="Set log level for logger: debug|info|warning|error.")

    args = parser.parse_args()

    logger.debug(f"Input with flags: {sys.argv}")
    logger.info("SubGrab script initialized")

    # LANGUAGE HANDLING
    PROVIDER = args.provider
    LANGUAGES = get_languages(PROVIDER)
    global LANGUAGE

    try:

        LANGUAGE = LANGUAGES[args.lang.lower()]
        print(f"LANGUAGE: {LANGUAGE}")
        logger.info(f"Language: {LANGUAGE['name']}")

    except KeyError:

        logger.error(f"Language {args.lang} not found. Either it's not supported by {args.provider}, or it's missing in subgrab language dictionary")

    # CLI ARGUMENT PROCESSING
    if args.silent:
        # If mode is silent
        logger.debug("Execute in Silent Mode")
        subscene.MODE = "silent"

    #if args.debug:
    #    cli.MODE = args.debug

    # (1) Process entered titles first, if entered.
    if args.media_name:

        soup = scrape_page(url=PROVIDER.SUB_QUERY,
                           parameter=args.media_name)

        titles_dict = PROVIDER.search_titles(soup)
        title_url = PROVIDER.select_title(titles_dict, LANGUAGE)

        soup = scrape_page(url=title_url)

        entries_dict = PROVIDER.get_entries(soup)
        print(entries_dict)

        # safe to json (to not have to crawl again)
        target = Path('.').joinpath('subtitles.json')
        if not target.exists():
            with open(target, 'w+') as f:
                json.dump(dict(entries_dict), f)

        entries_urls = PROVIDER.get_dl_pages(entries_dict, args.count)

        for url in entries_urls:
            PROVIDER.dl_sub(url)
        #PROVIDER.get_data(titles_dict)


    """
    if args.dir != ".":
        # Searches for movies in specified directory.
        logger.debug("Running in directory: {}".format(args.dir))
        try:
            os.chdir(args.dir)
            # Create folder for the files in the current
            directory.create_folder()
            # directory (which are not in a folder).
            directory.get_media_files()
            directory.dir_dl()
        except Exception as e:
            logger.debug("Invalid Directory Input - {}".format(e))
            print("Invalid Directory Input - {}".format(e))

    elif args.dir == "." and not args.media_name:
        # Searches for movies in current directory.
        directory.create_folder()
        directory.get_media_files()
        directory.dir_dl(sub_count=args.count)
    elif args.media_name:
        # Searches for the specified movie.
        args.media_name = " ".join(args.media_name)
        logger.info("Searching For: {}".format(args.media_name))
        sub_link = subscene.sel_title(name=args.media_name.replace(" ", "."))
        logger.info(
            "Subtitle Link for {} : {}".format(args.media_name, sub_link)
        )
        if sub_link:
            for i in subscene.sel_sub(
                page=sub_link, sub_count=args.count, name=args.media_name
            ):
                logger.debug("Downloading Subtitle: {}\n".format(i))
                subscene.dl_sub(i)

    else:
        print("Incorrect Arguments Specified.")
    """


if __name__ == "__main__":
    main()
