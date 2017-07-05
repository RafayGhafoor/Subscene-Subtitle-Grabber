# Subscene Subtitles Grabber:
This program makes your **Subtitles Search** easier by automating the process.

# Usage:

**For Custom Movie Subtitle Download:-**

```python
>>> python SubsceneDL.py -m Movie_Name
```
You can also specify movie year (which is the recommended way) for better precision.
```python
>>> python SubsceneDL.py -m Movie_Name -y Movie_Year
```
**For Downloading Movies Subtitles in Current Directory:-**

```python
>>> python SubsceneDL.py
```
You can also **specify** directory by putting -d flag and then directory_path

```python
>>> python SubsceneDL.py -d PATH
```

# TODO List:

- [x] Adding support for more languages.
- [x] Adding flags.
- [ ] AllSubDB, OpenSubtitles, YIFY subtitles search.
- [ ] Adding display mode for manual subtitle selection.
- [ ] Adding silent mode for downloading subtitles.
- [ ] Adding GUI box for subtitle sync check in the media-player (in individual mode).
- [ ] Use Logging.
- [ ] Implementation for seasons episodes.
- [ ] Auto-Sync (best-preferred subtitle) for movies.
- [ ] Different search algorithms implementation for precise results. 
- [ ] Integrating script with torrent clients.

# Requirements:

`pip install -r Requirements.txt`
- Python 2.7
- Requests, Beautiful Soup

# Installation:

Clone the repository by clicking on the Clone / Download Button.

`git clone https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber`
