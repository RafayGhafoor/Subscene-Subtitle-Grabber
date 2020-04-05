# SubGrab - Command-line Subtitles Downloader:

[![Downloads](http://pepy.tech/badge/subgrab)](http://pepy.tech/count/subgrab)

A utility which provides an ease for automating media i.e., Movies, TV-Series subtitle scraping from multiple providers.

# Index:

* [Installation](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#installation)
* [Preview](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#preview)
* [Requirements](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#requirements)
* [Supported Sites](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#providers-supported)
* [Preview](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#preview)
* [Usage](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#usage)
* [Examples](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#examples)
* [Features](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#features)
* [Changelog](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#changelog)
* [Features Upcoming](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#todo)

# Status/Version:

* Current Version: 1.0.2

# Installation:

`pip install subgrab`

# Preview:

[![asciicast](https://asciinema.org/a/316877.svg)](https://asciinema.org/a/316877)

# Providers Supported:

Following sites can be used for subtitle downloading:

<center>

|           Supported Sites            |
| :----------------------------------: |
|           SUBSCENE `(-m)`            |
| ALLSUBDB `(default for directories)` |

</center>

# Usage:

```
Usage:

subgrab [-h] [-d directory path] [-m Name of the movie/season] [-s Silent Mode]
                   [-c Number of Subtitles to be downloaded] [-l Custom language]

Options:

  -h, --help            Show this help message and exit.

  -d DIR, --dir DIR     Specify directory to work in.

  -m MOVIE_NAME [MOVIE_NAME ...], --movie-name MOVIE_NAME [MOVIE_NAME ...]
                        Provide Movie Name.

  -s, --silent          Silent mode.

  -c COUNT, --count COUNT
                        Number of subtitles to be downloaded.

  -l LANG, --lang LANG  Change language.
```

# Examples:

```python
subgrab                             # To run in current working directory.

subgrab -m Doctor Strange           # For custom movie subtitle download.

subgrab -m Doctor Strange -s        # Silent mode (No prompts i.e., title selection [if not found]).

subgrab -d "DIRECTORY_PATH"         # For specific directory.

subgrab -m The Intern 2015 -s -l AR # Language specified (First two characters of the language).

subgrab -m The Intern 2015 -c 3 -s  # Download 3 subtitles for the movie.
```

# Changelog:

* [Changelog](https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber/blob/master/changelog.rst)

# Note:

* (For Windows) To use it from the context menu, paste subtitle.bat file in "shell:sendto" (By typing this in RUN).
  Taken from Manojmj subtitles script.

# Features:

* Two Mode (CLI and Silent inside individual media downloading [-m]) - CLI mode is executed when the title (provided i.e. media name) is not recognized by the site. Mostly when year is not provied (when two or more media names collide). Silent mode is usually executed when year is provided in the argument. Optional, you can also specify silent mode argument - which forces to download subtitles without title selection prompt. The media argument (-m) followed by the silent mode (-s) argument forces silent mode.

* Subtitles count argument added which allows you to download multiple subtitles for an individual media. This is useful when the exact match is not found and you can download multiple srt files and check them if they are in sync with the media file (integrated in v0.12).

* Added multiple languages support (v0.12).

* Allows you to download subtitles for movies by specifying movie name and year (optional).

* Allows you to download subtitles for media files in a specified directory.

* Cross-platform (Tested on Linux and Windows).

* Logs generation on script execution (v0.15)

* Added Support for the SubDb (v0.16), now first preference for downloading subtitles is SubDB in downloading subtitles from a directory.

* Initial release (v1.0.0)

# TODO:

* [x] Adding support for more languages.
* [x] Adding flags.
* [x] Support for AllSubDB .
* [ ] Support for OpenSubtitles, YifySubtitles.
* [ ] Auto-Sync subtitle naming with the media file when downloaded from subscene.
* [ ] A GUI box which creates a dialogue box (consisting of tick and cross), which waits for the user to check if the subtitle downloaded is synchronized with media file or not - if clicked cross, downloads another subtitle (Process gets repeated unless, correctly synchronized).
* [ ] Watch-folder feature (runs as a service). # Useful for movies automatically downloaded on servers.
* [ ] Argument handling (Replace Argsparse with Click).
* [ ] Using Tabulate for monitoring directory subtitle downloading progress. Three Columns [#, Movie_Folder, Status].
* [ ] Better Logging.
* [ ] Download subtitles for movies contained in a directory of X year.
* [x] Adding silent mode for downloading subtitles.
* [x] Adding CLI mode for manually downloading subtitles.
* [x] Implement Logging.
* [x] Implementation for seasons episodes.
* [x] Different search algorithms implementation for precise results.
* [x] Improving CLI Mode by displaying the menu according to the site.
* [ ] Multiple subtitle language support also associated with the count variable.

```
For example:
>>> subgrab -m Doctor Strange -s -l AR, EN, SP -c 3
should download 3 subtitles for each language specified
```

* [ ] An option to print list of movies which has subtitles.
* [ ] Creating options in context menu.
* [ ] Display menu which enables to download subtitles for selected directories. (Supporting ranges)

```
For Examples:
(0) Movie 1
(1) Movie 2
.
.
(10) Movie 10
------------------------------------------------------------------------------------------------------
(Interactive Prompt)
> 1-3, 6,7,10

will download subtitles for the directories specified.
```
