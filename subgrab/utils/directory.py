import shutil
import os
import subgrab.providers.subscene as subscene
import subgrab.providers.subdb as subdb
import logging

logger = logging.getLogger("directory.py")
EXT = ['.mp4', '.mkv', '.avi', '.flv']
MOVIES_DIR = {}  # Contains Movies Directories (keys) and the
                 # files inside them (values = [list])
REMOVALS = []  # Which already contains subtitles

def create_folder():
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
                    logger.info("Moved to folder: %s" % (files.strip(extension)))
                    os.mkdir(files.strip(extension))
                    shutil.move(files, files.strip(extension))  # Moves the file to the new folder
                except (OSError, IOError):
                    logger.debug("Cannot create folder for: %s" % (files.strip(extension)))
                          # If folder exists for the filename or name which
                          # contains characters out of the ordinal range


def get_media_files():
    '''
    Obtains media files from the current/specified directory.
    '''
    # start_time = time.time()
    for folders, _, files in os.walk('.'):
        for i in files:
            folders = folders.replace('.' + os.sep, '')
            if i.endswith(".srt"):
                REMOVALS.append(folders)
            for extension in EXT:
                if i.endswith(extension):
                    if folders not in MOVIES_DIR:
                        MOVIES_DIR[folders] = []
                    MOVIES_DIR[folders].append(i)
    # Directories which contains .srt files (Subtitles)
    for i in REMOVALS:
        try:
            del(MOVIES_DIR[i])
        except KeyError:    # Already Removed if one srt file was found in folder
            pass
    # print("--- Function (GET_MEDIA_FILES) took %s seconds ---" % (time.time() - start_time))


def dir_dl(sub_count=1):
    '''
    Download subtitles for the movies in a directory.
    '''
    # start_time = time.time()
    cwd = os.getcwd()
    for folders, movies in MOVIES_DIR.items():
        os.chdir(folders)
        print("Downloading Subtitles for [%s]" % folders)
        logger.info("Downloading Subtitles for [%s]" % folders)
        for mov in movies:
            subdb_check = subdb.get_sub(file_hash=subdb.get_hash(mov), filename=mov, language='en')
            if subdb_check == 200:
                logger.info("Subtitle Downloaded for %s" % (mov))
                print(("Subtitle Downloaded for %s" %(mov)))

            elif subdb != 200:
                logger.info("Subtitles for [%s] not found on AllSubDB" % (mov))
                logger.info("Searching for subtitles on subscene - now")
                sub_link = subscene.sel_title(os.path.splitext(mov)[0])
                if sub_link:
                    if subscene.sel_sub(page=sub_link, name=mov):
                        for i in subscene.sel_sub(page=sub_link, sub_count=sub_count, name=mov):
                            subscene.dl_sub(i)
                    else:
                        print("Subtitle not found for [%s]" % (mov.capitalize()))
                        logger.debug("Subtitle not found for [%s]" % (mov))
                else:
                    print("Subtitle not found for [%s]" % (mov.capitalize()))
                    logger.debug("Subtitle not found for [%s]" % (mov))
        os.chdir(cwd)
    # print("--- Function (DOWNLOAD_SUB) took %s seconds ---" % (time.time() - start_time))
