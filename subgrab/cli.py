import argparse
import logging
import logging.config
import os
import sys

import pkg_resources

from config import init_logger
from subgrab.providers import subscene
from subgrab.utils import directory


def get_version():
    return pkg_resources.get_distribution("subgrab").version


def main():

    logger = init_logger()

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

    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version."
    )

    args = parser.parse_args()

    logger.debug("Input with flags: {}".format(sys.argv))

    logger.info("Initialized SubGrab script")

    if args.version:
        sys.exit(get_version())

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
