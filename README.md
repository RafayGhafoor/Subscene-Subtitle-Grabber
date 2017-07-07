# Subtitles Downloader:
This program makes your **Subtitles Search** easier by automating the process.

# Note:

- Script is being re-written. Currently supports subtitles download for individual movies.

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

# Requirements:

`pip install -r Requirements.txt`
- Python 2.7
- Requests, Beautiful Soup

