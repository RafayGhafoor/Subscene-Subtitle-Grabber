SubGrab - Command-line Subtitles Downloader:
============================================

A python\ *3* script that allows you to download subtitles for
TV-Series, Anime and Movies from multiple sites.

|Codacy Badge|

Index:
======

-  `Installation <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#Installation>`__
-  `Requirements <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#Requirements>`__
-  `Supported
   Sites <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#Providers-Supported>`__
-  `Preview <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#Preview>`__
-  `Usage <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#Usage>`__
-  `Examples <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#Examples>`__
-  `Features <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#Features>`__
-  `Changelog <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#Changelog>`__
-  `Features
   Upcoming <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber#TODO>`__

Status/Version:
===============

-  Beta Release.
-  Current Version: 0.17

Installation:
=============

-  Via Repo:

   ::

       git clone https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber
       cd Subscene-Subtitle-Grabber
       python setup.py install

-  Via PIP:

``pip install subgrab``

Preview:
========

|asciicast|

Providers Supported:
====================

Following sites can be used for subtitle downloading:

.. raw:: html

   <center>

+------------------------------------------+
| Supported Sites                          |
+==========================================+
| SUBSCENE ``(-m)``                        |
+------------------------------------------+
| ALLSUBDB ``(default for directories)``   |
+------------------------------------------+

.. raw:: html

   </center>

Usage:
======

::

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

Examples:
=========

.. code:: python

    subgrab                             # To run in current working directory.

    subgrab -m Doctor Strange           # For custom movie subtitle download.

    subgrab -m Doctor Strange -s        # Silent mode (No prompts i.e., title selection [if not found]).

    subgrab -d "DIRECTORY_PATH"         # For specific directory.

    subgrab -m The Intern 2015 -s -l AR # Language specified (First two characters of the language).

    subgrab -m The Intern 2015 -c 3 -s  # Download 3 subtitles for the movie.

Changelog:
==========

-  `Changelog <https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber/blob/dev/changelog.rst>`__

Note:
=====

-  (For Windows) To use it from the context menu, paste subtitle.bat
   file in "shell:sendto" (By typing this in RUN). Taken from Manojmj
   subtitles script.

Features:
=========

-  Two Mode (CLI and Silent inside individual media downloading [-m]) -
   CLI mode is executed when the title (provided i.e. media name) is not
   recognized by the site. Mostly when year is not provied (when two or
   more media names collide). Silent mode is usually executed when year
   is provided in the argument. Optional, you can also specify silent
   mode argument - which forces to download subtitles without title
   selection prompt. The media argument (-m) followed by the silent mode
   (-s) argument forces silent mode.

-  Subtitles count argument added which allows you to download multiple
   subtitles for an individual media. This is useful when the exact
   match is not found and you can download multiple srt files and check
   them if they are in sync with the media file (integrated in v0.12).

-  Added multiple languages support (v0.12).

-  Allows you to download subtitles for movies by specifying movie name
   and year (optional).

-  Allows you to download subtitles for media files in a specified
   directory.

-  Cross-platform (Tested on Linux and Windows).

-  Logs generation on script execution (v0.15)

-  Added Support for the SubDb (v0.16), now first preference for
   downloading subtitles is SubDB in downloading subtitles from a
   directory.

Requirements:
=============

-  Python 3
-  Requests
-  BeautifulSoup

TODO:
=====

-  [x] Adding support for more languages.
-  [x] Adding flags.
-  [X] Support for AllSubDB .
-  [ ] Support for OpenSubtitles, YifySubtitles.
-  [ ] Auto-Sync subtitle naming with the media file when downloaded
   from subscene.
-  [ ] A GUI box which creates a dialogue box (consisting of tick and
   cross), which waits for the user to check if the subtitle downloaded
   is synchronized with media file or not - if clicked cross, downloads
   another subtitle (Process gets repeated unless, correctly
   synchronized).
-  [ ] Watch-folder feature (runs as a service). # Useful for movies
   automatically downloaded on servers.
-  [ ] Argument handling (Replace Argsparse with Click).
-  [ ] Using Tabulate for monitoring directory subtitle downloading
   progress. Three Columns [#, Movie\_Folder, Status].
-  [ ] Better Logging.
-  [ ] Download subtitles for movies contained in a directory of X year.
-  [X] Adding silent mode for downloading subtitles.
-  [X] Adding CLI mode for manually downloading subtitles.
-  [X] Implement Logging.
-  [X] Implementation for seasons episodes.
-  [X] Different search algorithms implementation for precise results.
-  [X] Improving CLI Mode by displaying the menu according to the site.
-  [ ] Multiple subtitle language support also associated with the count
   variable.

::

    For example:
    >>> subgrab -m Doctor Strange -s -l AR, EN, SP -c 3
    should download 3 subtitles for each language specified

-  [ ] An option to print list of movies which has subtitles.
-  [ ] Creating options in context menu.
-  [ ] Display menu which enables to download subtitles for selected
   directories. (Supporting ranges)

::

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

.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/1f1ddff652d14f60bbf2f8d0b6c11cc8
   :target: https://www.codacy.com/app/RafayGhafoor/Subscene-Subtitle-Grabber?utm_source=github.com&utm_medium=referral&utm_content=RafayGhafoor/Subscene-Subtitle-Grabber&utm_campaign=Badge_Grade
.. |asciicast| image:: https://asciinema.org/a/4tZ08jjH7yeITtYK6bpsrH5c5.png
   :target: https://asciinema.org/a/4tZ08jjH7yeITtYK6bpsrH5c5?speed=2
