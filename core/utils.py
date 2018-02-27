import shutil
import os

EXT = ['.mp4', '.mkv', '.avi', '.flv']
SUB_EXT = ['.srt', '.ass']


def fix_media():
    '''Search for media extensions in current directory and move them in a folder.'''
    for files in [i for extension in EXT for i in os.listdir('.') if extension in i]:
        for extension in EXT:
            if files.endswith(extension):
                # Creates a folder of same name as file (excluding file extension)
                try:
                    os.mkdir(files.strip(extension))
                    shutil.move(files, files.strip(extension))  # Moves the file to the new folder
                except (OSError, IOError):
                    #TODO: Write log message.
                    pass
                          # If folder exists for the filename or name which
                          # contains characters out of the ordinal range


def scan_media(crawl_dir='.'):
    '''Scans media files (without subtitles) in current directory.'''
    movies = {}     # media path --> keys
                    # media files (inside that path) --> values (a list)

    for folders, _, files in os.walk(crawl_dir):
        if all(map(lambda media_ext: os.path.splitext(media_ext)[1] not in SUB_EXT, files)) and files:
            folders = folders.replace(('.' + os.sep), '')   # Cleans path by removing leading relative path.

            if folders not in movies:
                movies[folders] = []

            movies[folders].extend(files)

    return {k: [i for ext in EXT for i in v if i.endswith(ext)] for k,v in movies.items()}



if __name__ == '__main__':
    os.chdir('/home/rafay/Desktop/Movies')
    for k,v in scan_media().items():
        print('{}\t{}'.format(k,v))
