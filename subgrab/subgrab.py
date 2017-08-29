import os
import directory
import source.subscene as subscene
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='.', help='Specify directory to work in.')
    parser.add_argument('-m', '--movie-name', nargs='+', help='Provide movie name.')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode.')
    parser.add_argument('-c', '--count', type=int, default=1, help='Number of subtitles to be downloaded.')
    parser.add_argument('-l', '--lang', default='EN', help='Change language.')
    args = parser.parse_args()

    if args.silent:
        subscene.MODE = "silent"

    if args.lang:
        subscene.DEFAULT_LANG = subscene.LANGUAGE[args.lang]

    if args.dir != '.':
        # Searches for movies in current directory.
        directory.create_folder()
        # print "%r" % args.dir
        try:
            os.chdir(args.dir)
            directory.get_media_files()
            directory.dir_dl()
        except Exception as e:
            print 'Invalid Directory Input.', e

    elif args.dir == '.' and not args.movie_name:
        # Searches for movies in specified directory.
        directory.create_folder()
        directory.get_media_files()
        directory.dir_dl(sub_count=args.count)

    elif args.movie_name:
        # print args.movie_name
        args.movie_name = ' '.join(args.movie_name)
        sub_link = subscene.select_title(name=args.movie_name.replace(' ', '.'))
        # print sub_link
        if sub_link:
            for i in subscene.sel_sub(page=sub_link, sub_count=args.count):
                subscene.dl_sub(i)

    else:
        print 'Incorrect Arguments Specified.'
