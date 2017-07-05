import requests
import bs4


SUB_QUERY = "https://subscene.com/subtitles/title"
SUB_COMMENTS = {"Perfect Sync": 10, "Update": 2, "Thanks": 6, "Fixed": 4}
SCORING = ""


def scrape_page(url, parameter=''):
    '''Allows you to get content from a url.'''
    if parameter:
        req = requests.get(url, {'q': parameter})
    else:
        req = requests.get(url)
    # print 'Generated URL is ---> %r\n' % r.url
    req_html = bs4.BeautifulSoup(req.content, "lxml")
    return req_html


def get_title(html_content):
    '''
    Gets media name titles from subscene site.
    '''
    if html_content.find('div', {"class": "search-result"}).h2.string == "No results found":
        print "Sorry, the subtitles for this media file aren't available."
        return
    return html_content.findAll("div", {"class": "search-result"})
    

def sel_title_name(title_lst, name='', year='', mode=1):
    '''
    Select title of the media (i.e., Movie, TV-Series)
    :param title_lst: Title Names from the function get_title
    :param name: Media Name. For Example: "Doctor Strange"
    :param year: Media Year. For Example: "2016"
    :param mode: Select CLI Mode or Silent Mode.
    '''
    if not name and not year:
        print "Invalid Input."
        return
        
    for titles in title_lst:
        print titles
        popular = titles.find("h2", {"class": "popular"}) # Searches for the popular tag
        if mode == 1:
            title_link = silent_mode(titles, name=name, year=year)
            return title_link
        else:
            return cli_mode(titles)
        

def silent_mode(title_name, name='', year=''):
    '''
    An automatic mode for selecting media title from subscene site.
    :param title_name: title names obtained from get_title function.
    '''

    def html_navigator(category="Popular"):
        '''
        Navigates html tree and select title from it. This function is
        called twice. For example, the default (Popular) category for
        searching in is Popular. It will search title first in popular
        category and then in other categories. If default category
        changes, this process is reversed.
        :param category: selects which category should be searched first in
        the html tree.
        '''
        popular = title_name.find("h2", {"class": "popular"})
        if category == "Popular": # Searches in Popular Category and the categories next to it.
            section = popular.find_all_next("div", {"class": "title"})
        else: # Searches in categories above popular tag.
            section = titles.find_all("div", {"class": "title"})
        for results in section:
            match = 1        
            for letter in name.split():            
                if letter.lower() in results.a.text.lower() and year in results.a.text.lower():
                    if len(name.split()) == match:
                        return "https://subscene.com" + results.a.get("href")
                    match += 1

    # Searches first in Popular category, if found, returns the title name
    obt_link = html_navigator(category="Popular")
    if not obt_link:    # If not found in the popular category, searches in other category
        return html_navigator(category="n_popular")
    return obt_link

                
def cli_mode(titles_name):    
    '''
    A manual mode driven by user, allows user to select subtitles manually
    from the command-line.
    :param titles_name: title names obtained from get_title function.
    '''
    media_titles = [] # Contains key names of titles_and_links dictionary.
    titles_and_links = {} # --> "Doctor Strange" --> "https://subscene.com/.../1345632"
    popular = titles_name.find("h2", {"class": "popular"})
    
    for i, x in enumerate(popular.find_all_next("div", {"class": "title"})):
        titles_and_links[x.text.strip()] = x.a.get("href") 
        print "(%s): %s" % (i, x.text.strip())
        media_titles.append(x.text.strip())        
    
    qs = int(raw_input("Please Enter Movie Number: ")) 
    return "https://subscene.com" + titles_and_links[media_titles[qs]]
                    
    
if __name__ == "__main__":
    soup = scrape_page(url=SUB_QUERY, parameter="sherlock third season")
    titles = get_title(soup)
    sub_link = sel_title_name(titles, name="sherlock second season", year="", mode=2)
    print sub_link
