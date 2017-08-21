import directory
import source.subscene as subscene
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default = '.', help = 'Specify directory to work in')
    parser.add_argument('-m', '--movie-name', nargs='+', help = 'Provide Movie Name')
    parser.add_argument('-y', '--movie-year', help = 'Provide Movie Year for better precision.')
    args = parser.parse_args()

    if args.movie_name:
        args.movie_name = ' '.join(args.movie_name)

    if args.dir != '.':
        '''Searches for Movies in Current Directory'''
        create_folder()
        try:
            os.chdir(args.dir)
            directory.get_media_files()
            subscene.dir_dl()
        except:
            print 'Invalid Directory Input.'

    elif args.dir == '.' and not args.movie_name:
        '''Searches for Movies in Specified Directory'''
        create_folder()
        directory.get_media_files()
        subscene.dir_dl()

    elif args.movie_name:
        '''Searches for the movie Specified by Name'''
        if args.movie_year:
            # Runs in CLI mode
            sub_link = subscene.sel_sub('https://subscene.com/subtitles/release?q=' + args.movie_name)
            if not sub_link:
                sub_link = subscene.select_title(name=args.movie_name, year=args.movie_year, mode=1)
                for i in subscene.sel_sub(sub_link):
                    subscene.dl_sub(i)
            for i in sub_link:
                subscene.dl_sub(i)
        else:
            # Runs in Silent mode
            sub_link = subscene.sel_sub('https://subscene.com/subtitles/release?q=' + args.movie_name)
            if not sub_link:
                sub_link = subscene.select_title(name=args.movie_name, mode=2)
                for i in subscene.sel_sub(sub_link):
                    subscene.dl_sub(i)
            for i in sub_link:
                subscene.dl_sub(i)

    else:
        'Incorrect Arguments Specified.'


if __name__ == "__main__":
    main()
