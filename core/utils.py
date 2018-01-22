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


def get_media(location='.'):
    '''Get media files from the current directory.'''
    movies = {}     # Contains Movies Directories (keys) and the
                     # files inside them (values = [list])
    srt_files = []  # Contains files with subtitles already

    for folders, _, files in os.walk(location):
        for media in files:
            folders = folders.replace(('.' + os.sep), '')   # Cleans path by removing leading relative path.
            if os.path.splitext(media)[1] in EXT:
                if folders not in movies:
                    movies[folders] = []
                movies[folders].append(media)
            elif media.endswith('.srt'):
                srt_files.append(folders.replace('.' + os.sep, ''))

    # Clean movies which already have subtitles.
    for movie_with_sub in srt_files:
        if movie_with_sub in movies:
            del movies[movie_with_sub]

    return movies
