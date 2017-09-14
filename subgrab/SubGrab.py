import subgrab.utils.directory as directory
import subgrab.providers.subscene as subscene
import argparse
import sys
import logging
import os

if os.sep == "\\": # Windows OS
    log_home = os.path.expanduser(os.path.join(os.path.join('~', 'AppData'), 'Local'))
else: # Other than Windows
    log_home = os.getenv('XDG_DATA_HOME', os.path.expanduser(os.path.join(os.path.join('~', '.local'), 'share')))
log_directory = os.path.join(log_home, 'Subgrab')
if not os.path.exists(log_directory):
    os.mkdir(log_directory)
logfile_name = os.path.join(log_directory, "subgrab.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(logfile_name)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='.', help='Specify directory to work in.')
    parser.add_argument('-m', '--media-name', nargs='+', help='Provide movie name.')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode.')
    parser.add_argument('-c', '--count', type=int, default=1, help='Number of subtitles to be downloaded.')
    parser.add_argument('-l', '--lang', default='EN', help='Change language.')
    args = parser.parse_args()
    logger.debug("Input with flags: %s" % (sys.argv))
    logger.info("Initialized SubGrab script")
    if args.silent:
        # If mode is silent
        logger.debug("Executing Silent Mode")
        subscene.MODE = "silent"

    if args.lang:
        # Select language - Enter first two letters of the language
        if len(args.lang) == 2:
            subscene.DEFAULT_LANG = subscene.LANGUAGE[args.lang.upper()]
            logger.info("Set Language: %s" % (args.lang))
        else:
            sys.exit("Invalid language specified.")

    if args.dir != '.':
        # Searches for movies in specified directory.
        directory.create_folder()   # Create folder for the files in the current
                                    # directory (which are not in a folder).
        logger.debug("Running in directory: %s" % (args.dir))
        try:
            os.chdir(args.dir)
            directory.get_media_files()
            directory.dir_dl()
        except Exception as e:
            print 'Invalid Directory Input.', e

    elif args.dir == '.' and not args.media_name:
        # Searches for movies in current directory.
        directory.create_folder()
        directory.get_media_files()
        directory.dir_dl(sub_count=args.count)

    elif args.media_name:
        # Searches for the specified movie.
        args.media_name = ' '.join(args.media_name)
        logger.info("Searching For: %s" % (args.media_name))
        sub_link = subscene.sel_title(name=args.media_name.replace(' ', '.'))
        logger.info("Subtitle Link for %s : %s" % (args.media_name, sub_link))
        # print sub_link
        if sub_link:
            for i in subscene.sel_sub(page=sub_link, sub_count=args.count, name=args.media_name):
                logger.debug("Downloading Subtitle: %s\n" % (i))
                subscene.dl_sub(i)

    else:
        print 'Incorrect Arguments Specified.'
