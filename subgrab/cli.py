import argparse
import logging
import logging.config
import os
import sys

from subgrab.providers import subscene
from subgrab.utils import directory


if os.sep == "\\":  # Windows OS
    log_home = os.path.expanduser(
        os.path.join(os.path.join("~", "AppData"), "Local")
    )
else:  # Other than Windows
    log_home = os.getenv(
        "XDG_DATA_HOME",
        os.path.expanduser(os.path.join(os.path.join("~", ".local"), "share")),
    )
log_directory = os.path.join(log_home, "Subgrab")

if not os.path.exists(log_directory):
    os.mkdir(log_directory)

logfile_name = os.path.join(log_directory, "subgrab.log")
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
        "SubGrab": {"handlers": ["file"], "level": "DEBUG", "propagate": True},
        "directory": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "subscene": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger("SubGrab")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dir", default=".", help="Specify directory to work in."
    )
    parser.add_argument(
        "-m", "--media-name", nargs="+", help="Provide movie name."
    )
    parser.add_argument(
        "-s", "--silent", action="store_true", help="Silent mode."
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="Number of subtitles to be downloaded.",
    )
    parser.add_argument("-l", "--lang", default="EN", help="Change language.")
    args = parser.parse_args()
    logger.debug("Input with flags: {}".format(sys.argv))
    logger.info("Initialized SubGrab script")

    if args.silent:
        # If mode is silent
        logger.debug("Executing Silent Mode")
        subscene.MODE = "silent"

    if args.lang:
        # Select language - Enter first two letters of the language
        if len(args.lang) == 2:
            subscene.DEFAULT_LANG = subscene.LANGUAGE[args.lang.upper()]
            logger.info("Set Language: {}".format(args.lang))
        else:
            sys.exit("Invalid language specified.")

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


if __name__ == "__main__":
    main()
