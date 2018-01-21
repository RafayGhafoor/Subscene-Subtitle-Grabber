import shutil
import os
# import core.providers.subscene as subscene
# import core.providers.subdb as subdb
os.chdir(r'C:\Users\Habiba Ghafoor\Downloads\The.Mountain.Between.Us.2017.BDRip.x264-DRONES[EtMovies]')
EXT = ['.mp4', '.mkv', '.avi', '.flv']
REMOVALS = []  # Which already contains subtitles

def get_media():
    movies = {}     # Contains Movies Directories (keys) and the
                     # files inside them (values = [list])
    srt_files = []  # Contains files with subtitles already
    for folders, _, files in os.walk('.'):
        for i in files:
            if os.path.splitext(i)[1] in EXT:
                if folders.replace(('.' + os.sep), '') not in movies:
                    movies[folders] = []
                movies[folders].append(i)
            elif i.endswith('.srt'):
                srt_files.append(folders.replace('.' + os.sep, ''))
    return movies

f = get_media()
print(f)
#
# def get_media_files():
#     '''
#     Obtains media files from the current/specified directory.
#     '''
#     for folders, _, files in os.walk('.'):
#         for i in files:
#             folders = folders.replace('.' + os.sep, '')
#             if i.endswith(".srt"):
#                 REMOVALS.append(folders)
#             for extension in EXT:
#                 if i.endswith(extension):
#                     if folders not in MOVIES_DIR:
#                         MOVIES_DIR[folders] = []
#                     MOVIES_DIR[folders].append(i)
#     # Directories which contains .srt files (Subtitles)
#     for i in REMOVALS:
#         if i in MOVIES_DIR: # a check for the presence of key which can be already removed or not present
#             del(MOVIES_DIR[i])
#
#
#
# def dir_dl(sub_count=1):
#     '''
#     Download subtitles for the movies in a directory.
#     '''
#     # start_time = time.time()
#     cwd = os.getcwd()
#     for folders, movies in MOVIES_DIR.items():
#         os.chdir(folders)
#         print("Downloading Subtitles for [{}]".format(folders))
#         logger.info("Downloading Subtitles for [{}]".format(folders))
#         for mov in movies:
#             subdb_check = subdb.get_sub(file_hash=subdb.get_hash(mov), filename=mov, language='en')
#             if subdb_check == 200:
#                 logger.info("Subtitle Downloaded for {}".format(mov))
#                 print(("Subtitle Downloaded for {}".format(mov)))
#
#             elif subdb != 200:
#                 logger.info("Subtitles for [{}] not found on AllSubDB".format(mov))
#                 logger.info("Searching for subtitles on subscene - now")
#                 sub_link = subscene.sel_title(os.path.splitext(mov)[0])
#                 if sub_link:
#                     # Remove extension from mov argument
#                     selected_sub = subscene.sel_sub(page=sub_link, name=os.path.splitext(mov)[0])
#                     if selected_sub:
#                         for i in selected_sub:
#                             subscene.dl_sub(i)
#                     else:
#                         print("Subtitle not found for [{}]".format(mov.capitalize()))
#                         logger.debug("Subtitle not found for [{}]".format(mov))
#                 else:
#                     print("Subtitle not found for [{}]".format(mov.capitalize()))
#                     logger.debug("Subtitle not found for [{}]".format(mov))
#         os.chdir(cwd)
