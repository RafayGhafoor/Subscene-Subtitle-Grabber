'''
A provider base class which defines template for the subtitle sites.
'''

# Using lists because it's also used for prioritizing subtitle Downloading
# for example, the subtitles will be first searched on subscene, then allsubdb..
import logging
import requests
import bs4

PROVIDERS = [
"subscene", "allsubdb",
"opensubtitles", "legendastv"
]                 # More to be added

PROVIDERS_SUPPORTED_LANGUAGES = {
'subscene': (
             'Arabic', 'Burmese','Danish',
             'Dutch', 'English', 'Farsi_persian',
             'Indonesian', 'Italian', 'Malay',
             'Spanish', 'Vietnamese'
            ),

'allsubdb': (
            'en', 'es', 'fr',
            'it', 'nl', 'pl',
            'pt', 'ro', 'sv',
            'tr'
            )
}

class Provider:
    '''
    A base class for providers.
    '''
    def __init__(self, provider_name, base_url, logger_name, default_lang = "EN"):
        self.base_url = base_url
        self.default_lang = default_lang
        self.logger = logging.getLogger(logger_name)


    def scrape_page(self, url, soup="yes"):
        '''
        Retrieve content from a url.

        Parameters:

        url  :: URL to be scraped
        soup :: Create soup object using bs4 - defaults for yes
        '''
        HEADERS = {'User-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        req = requests.get(url, headers=HEADERS)
        if req.status_code != 200:
            logger.debug("{} not retrieved. Status code {} returned.".format(req.url, req.status_code))
            return
        if soup == "yes":
            req_html = bs4.BeautifulSoup(req.content, "lxml")
            return req_html
        else:
            return req.content


    def url_format(self, base_url, query, replacor="+"):
        '''
        Formats the url, provided with search string.

        Parameters:

        base_url :: URL of the provider
        query    :: The term to be searcher for
        replacor :: Character used for formatting url

        Example:
                base_url | query | replacor
        feed   --> https://subscene.com/subtitles/?q= | media name | .
        return --> https://subscene.com/subtitles/?q=media.name
        '''
        return base_url + query.replace(" ", replacor)


    def get_lang(self, provider_name):
        '''
        Get languages for a specific provider.

        Parameters:

        provider_name :: Provider name for subtitle site
        '''
        if provider_name in PROVIDERS:
            if provider_name == 'subscene':
                return PROVIDERS_SUPPORTED_LANGUAGES['subscene']
            elif provider_name == 'allsubdb':
                return PROVIDERS_SUPPORTED_LANGUAGES['allsubdb']
        else:
            print("Invalid provider name specified.")


    def downloader(self, download_url, filename):
        '''
        A downloader method which is used for every provider.

        Parameters:

        download_url :: URL for subtitle file
        filename     :: Filename for the subtitle file
        '''
        r = requests.get(download_url, stream=True)
        if not filename:
            filename = re.findall("filename=(.+)", r.headers['content-disposition'])[0]
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=150):
                    if chunk:
                        f.write(chunk)
        return filename
