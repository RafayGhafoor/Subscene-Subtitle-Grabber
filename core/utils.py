import shutil
import os

EXT = ['.mp4', '.mkv', '.avi', '.flv']


def create_dirs():
    '''
    Search for video extensions inside the current
    directory and If any of the files ending with such
    extensions are found (not in folder), create folder
    for them and paste the respective file in the corresponding
    folder.
    '''
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


def get_media(crawl_dir='.'):
    '''Get media files from the current directory.'''
    movies = {}     # Contains movies directories path (keys) and the
                     # files inside them (values = [list])
    srt_files = []  # Contains files with subtitles already

    for folders, _, files in os.walk(crawl_dir):
        for media in files:
            folders = folders.replace(('.' + os.sep), '')   # Cleans path by removing leading relative path.
            # scans directory for media files and those which have subtitles
            if os.path.splitext(media)[1] in EXT:
                if folders not in movies:
                    movies[folders] = []
                movies[folders].append(media)

            elif media.endswith('.srt'):
                srt_files.append(folders.replace('.' + os.sep, ''))

    # returns media files which doesn't have subtitles
    return {k: v for k, v in movies.items() if k not in srt_files}
