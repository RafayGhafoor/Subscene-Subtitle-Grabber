Subtitles [Subscene] Grabber (Sub-Grab v0.14):
==============================================

A script that allows you to download subtitles for TV-Series, Anime and
Movies from subscene site.

Status:
=======

-  Beta Release.

Installation:
=============

``pip install subgrab``

Preview:
========

|asciicast|

Usage:
======

::

    Usage:

    subgrab [-h] [-d DIR] [-m MEDIA_NAME [MEDIA_NAME ...]] [-s]
                       [-c COUNT] [-l LANG]

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

    subgrab -d DIRECTORY_PATH           # For specific directory.

    subgrab -m The Intern 2015 -s -l AR # Language specified (First two characters of the language).

    subgrab -m The Intern 2015 -c 3 -s  # Download 3 subtitles for the movie.

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

Requirements:
=============

-  Python v2.7
-  Requests
-  Beautiful Soup

TODO:
=====

-  [x] Adding support for more languages.
-  [x] Adding flags.
-  [ ] AllSubDB, OpenSubtitles, YIFY subtitles search.
-  [X] Adding silent mode for downloading subtitles.
-  [X] Adding CLI mode for manually downloading subtitles.
-  [ ] Adding GUI box for subtitle sync check in the media-player (in
   individual mode).
-  [ ] Use Logging.
-  [X] Optimize Code.
-  [X] Implementation for seasons episodes.
-  [X] Different search algorithms implementation for precise

.. |asciicast| image:: https://asciinema.org/a/0YutiMbCtvvoGtlEvJxKonL1L.png
   :target: https://asciinema.org/a/0YutiMbCtvvoGtlEvJxKonL1L