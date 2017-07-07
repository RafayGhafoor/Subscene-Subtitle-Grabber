import requests
import bs4

SUB_QUERY = "https://subscene.com/subtitles/title"

def scrape_page(url, parameter=''):
    '''Allows you to get content from a url.'''
    if parameter:
        req = requests.get(url, {'q': parameter})
    else:
        req = requests.get(url)
    # print 'Generated URL is ---> %r\n' % r.url
    req_html = bs4.BeautifulSoup(req.content, "lxml")
    return req_html