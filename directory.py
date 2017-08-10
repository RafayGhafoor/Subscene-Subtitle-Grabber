import os
import zipfile

REAL_DIRECTORY = []
EXT = ['.mp4', '.mkv', '.avi', '.flv']
ACTIVEDIR_FILES = [i for extension in EXT for i in os.listdir('.') if extension in i]
OSWALK_FOLDERS = []
OSWALK_FILES = []

for folders, subfolders, files in os.walk('.'):
    OSWALK_FOLDERS.append(folders)
    for i in files:
        OSWALK_FILES.append(i)


def zip_extractor(name):
    '''Extracts zip file obtained from the Subscene site (which contains subtitles).'''
    try:
        with zipfile.ZipFile(name, "r") as z:
            z.extractall(".")
        os.remove(name)
    except:
        pass


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
                else:
                    continue


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


def remove_ext(name):
    '''Removes extension from the movie file name.
    For example:-
    >>> Doctor.Strange.2016.mp4 [INPUT]
    >>> Doctor.Strange.2016 [RETURN]'''
    global ext
    for extension in EXT:
        if extension in name:
            return name.replace(extension,'')
            break
    return name


def name_grabber(medialst):
	'''Gets the Movie Name and Year from the filename and other meta
	data is removed.
	For Example:
	>>> Doctor.Strange.2016.720p.BrRip.mkv [INPUT]
	>>> Doctor Strange 2016 [RETURN]
	This is done for obtaining better search result from the subscene site.'''
	nameslist = []
	for movies in medialst:
		try:
			year = get_year(movies)
            # This is 2016 Movie --> This is | 2016 | Movie
            prev, found, removal = movies.partition(year)
            nameslist.append(prev.strip() + ' ' + year)
        except AttributeError:
            # If year not found in movie name
            nameslist.append(movies.strip())
            continue
    return nameslist


if __name__ == "__main__":
    create_folder()