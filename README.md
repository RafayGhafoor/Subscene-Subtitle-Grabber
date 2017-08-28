# Subtitles Downloader:
This program makes your subtitles **Search and Download** easier by automating the process.

# Status:

- Beta Release.

# Installation:

`pip install subgrab`

# Preview:

[![asciicast](https://asciinema.org/a/VfwNmIMiqmjVuku02FEUiImAT.png)](https://asciinema.org/a/VfwNmIMiqmjVuku02FEUiImAT)

# Usage:

```
usage: subgrab [-h] [-d DIR] [-m MOVIE_NAME [MOVIE_NAME ...]] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Specify directory to work in
  -m MOVIE_NAME [MOVIE_NAME ...], --movie-name MOVIE_NAME [MOVIE_NAME ...]
                        Provide Movie Name
  -s, --silent          Silent mode.
```

# Examples:

- **For custom movie subtitle download:-**

`subgrab -m Doctor Strange`

- **Silent mode (No prompts i.e., title selection (if not found))** 

`subgrab -m Doctor Strange -s`

- **To run in current working directory**

`subgrab`

- **For specific directory**

`subgrab -d DIRECTORY_PATH`

# Features:

- Allows you to download subtitles for movies by specifying movie name and year (optional).
- Allows you to download subtitles for media files in a specified directory.

# Requirements:

- Python 2.7
- Requests
- Beautiful Soup

# TODO:

- [x] Adding support for more languages.
- [x] Adding flags.
- [ ] AllSubDB, OpenSubtitles, YIFY subtitles search.
- [X] Adding silent mode for downloading subtitles.
- [X] Adding CLI mode for manually downloading subtitles.
- [ ] Adding GUI box for subtitle sync check in the media-player (in individual mode).
- [ ] Use Logging.
- [X] Optimize Code.
- [X] Implementation for seasons episodes.
- [X] Different search algorithms implementation for precise results. 
- [ ] Integrating script with torrent clients.
- [X] Improving CLI Mode by displaying the menu according to the site.
