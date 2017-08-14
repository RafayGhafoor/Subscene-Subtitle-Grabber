import re
import shutil
import os
import zipfile
import subscene
os.chdir("C:\Users\Habiba Ghafoor\Downloads\Movies")
EXT = ['.mp4', '.mkv', '.avi', '.flv']
ACTIVEDIR_FILES = [i for extension in EXT for i in os.listdir('.') if extension in i]
MOVIES_DIR = {}
REMOVALS = [] # Which already contains subtitles

def create_folder():
    '''
    Search for video extensions inside the current
    directory and If any of the files ending with such
    extensions are found (not in folder), create folder
    for them and paste the respective file in the corresponding
    folder.
    '''
    for files in ACTIVEDIR_FILES:
        for extension in EXT:
                if files.endswith(extension):
                    # Creates a folder of same name as file (excluding file extension)
                    try:
                        os.mkdir(files.strip(extension))
                        shutil.move(files, files.strip(extension))  # Moves the file to the new folder
                    except OSError:
                        pass  # If folder exists for the filename


def get_media_files():
    import time
    start_time = time.time()
    for folders, subfolders, files in os.walk('.'):
        for i in files:
            folders = folders.replace('.\\', '')
            if i.endswith(".srt"):
                REMOVALS.append(folders)
            for extension in EXT:
                if i.endswith(extension):
                    MOVIES_DIR[folders] = []
                    MOVIES_DIR[folders].append(i)
    print("--- Function (GET_MEDIA_FILES) took %s seconds ---" % (time.time() - start_time))


def get_year(filename):
    '''Obtains year from the movie filename.
    For example:-
    >>> Doctor.Strange.[2016].BrRip.720p.YIFY.mp4
    gets (2016) from the media file.'''
    # Searches for FOUR digits in the movie name, if found returns them.
    year_pattern = re.compile(r'(?!1080|2160)\d{4}')
    if year_pattern.search(filename):
        return year_pattern.search(filename).group()
    return filename


def download_sub():
    import time
    start_time = time.time()
    cwd = os.getcwd()
    for folders, movies in MOVIES_DIR.iteritems():
        # os.chdir(folders)
        for mov in movies:
            try:
                prev, year, removals = mov.partition(get_year(mov))
                sub_link = subscene.select_title(name=prev.replace('.', ' ').strip(), year=year)
            except: # Year not found
                sub_link = subscene.select_title(name=mov)
            if sub_link:
                for i in subscene.sel_sub(sub_link):
                    subscene.dl_sub(i)
        os.chdir(cwd)
    print("--- Function (DOWNLOAD_SUB) took %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    create_folder()
    get_media_files()
    for i in REMOVALS:
        del(MOVIES_DIR[i])
    print MOVIES_DIR
    # download_sub()
