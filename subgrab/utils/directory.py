import logging
import os
import shutil
from typing import Dict, List

from subgrab.providers import subdb, subscene


logger = logging.getLogger("directory.py")
EXT = [".mp4", ".mkv", ".avi", ".flv"]
MOVIES_DIR: Dict[str, List] = {}  # Contains Movies Directories (keys) and the
# files inside them (values = [list])
REMOVALS = []  # Which already contains subtitles


def create_folder():
    """
    Search for video extensions inside the current
    directory and If any of the files ending with such
    extensions are found (not in folder), create folder
    for them and paste the respective file in the corresponding
    folder.
    """
    for files in [
        i for extension in EXT for i in os.listdir(".") if extension in i
    ]:
        for extension in EXT:
            if files.endswith(extension):
                # Creates a folder of same name as file (excluding file extension)
                try:
                    logger.info(
                        "Moved to folder: {}".format(files.strip(extension))
                    )
                    os.mkdir(files.strip(extension))
                    shutil.move(
                        files, files.strip(extension)
                    )  # Moves the file to the new folder
                except (OSError, IOError):
                    logger.debug(
                        "Cannot create folder for: {}".format(
                            files.strip(extension)
                        )
                    )
                    # If folder exists for the filename or name which
                    # contains characters out of the ordinal range


def get_media_files():
    """
    Obtains media files from the current/specified directory.
    """
    for folders, _, files in os.walk("."):
        for i in files:
            folders = folders.replace("." + os.sep, "")
            if i.endswith(".srt"):
                REMOVALS.append(folders)
            for extension in EXT:
                if i.endswith(extension):
                    if folders not in MOVIES_DIR:
                        MOVIES_DIR[folders] = []
                    MOVIES_DIR[folders].append(i)
    # Directories which contains .srt files (Subtitles)
    for i in REMOVALS:
        if MOVIES_DIR.get(
            i
        ):  # a check for the presence of key which can be already removed or not present
            del MOVIES_DIR[i]


def dir_dl(sub_count=1):
    """
    Download subtitles for the movies in a directory.
    """
    # start_time = time.time()
    cwd = os.getcwd()
    for folders, movies in MOVIES_DIR.items():
        os.chdir(folders)
        print("Downloading Subtitles for [{}]".format(folders))
        logger.info("Downloading Subtitles for [{}]".format(folders))
        for mov in movies:
            subdb_check = subdb.get_sub(
                file_hash=subdb.get_hash(mov), filename=mov, language="en"
            )
            if subdb_check == 200:
                logger.info("Subtitle Downloaded for {}".format(mov))
                print("Subtitle Downloaded for {}".format(mov))

            elif subdb != 200:
                logger.info(
                    "Subtitles for [{}] not found on AllSubDB".format(mov)
                )
                logger.info("Searching for subtitles on subscene - now")
                sub_link = subscene.sel_title(os.path.splitext(mov)[0])
                if sub_link:
                    # Remove extension from mov argument
                    selected_sub = subscene.sel_sub(
                        page=sub_link, name=os.path.splitext(mov)[0]
                    )
                    if selected_sub:
                        for i in selected_sub:
                            subscene.dl_sub(i)
                    else:
                        print(
                            "Subtitle not found for [{}]".format(
                                mov.capitalize()
                            )
                        )
                        logger.debug("Subtitle not found for [{}]".format(mov))
                else:
                    print(
                        "Subtitle not found for [{}]".format(mov.capitalize())
                    )
                    logger.debug("Subtitle not found for [{}]".format(mov))
        os.chdir(cwd)
