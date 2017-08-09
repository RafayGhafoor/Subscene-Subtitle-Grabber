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

# Select Subtitles
def sel_sub(page, sub_count=1):
    r = scrape_page(page)
    sub_list = []
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    for link in soup.find_all('td', {'class': 'a1'}):
        for down_link in link.find_all('a'):
                if active_sub < sub_count:
                    if 'Trailer' not in link.text and language in eng_link.text:
                        if down_link.get('href') not in sub_list:
                            sub_list.append(down_link.get('href'))
                            active_sub += 1
    return ['https://subscene.com' + i for i in sub_list]
