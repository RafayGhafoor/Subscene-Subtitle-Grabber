import os
import subgrab.modules.directory as directory
import subgrab.source.subscene as subscene
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='.', help='Specify directory to work in.')
    parser.add_argument('-m', '--media-name', nargs='+', help='Provide movie name.')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode.')
    parser.add_argument('-c', '--count', type=int, default=1, help='Number of subtitles to be downloaded.')
    parser.add_argument('-l', '--lang', default='EN', help='Change language.')
    args = parser.parse_args()

    if args.silent:
        # If mode is silent
        subscene.MODE = "silent"

    if args.lang:
        # Select language - Enter first two letters of the language
        if len(args.lang) == 2:
            subscene.DEFAULT_LANG = subscene.LANGUAGE[args.lang.upper()]
        else:
            sys.exit("Invalid language specified.")

    if args.dir != '.':
        # Searches for movies in specified directory.
        directory.create_folder()   # Create folder for the files in the current
                                    # directory (which are not in a folder).
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
        sub_link = subscene.sel_title(name=args.media_name.replace(' ', '.'))
        # print sub_link
        if sub_link:
            for i in subscene.sel_sub(page=sub_link, sub_count=args.count, name=args.media_name):
                subscene.dl_sub(i)

    else:
        print 'Incorrect Arguments Specified.'
