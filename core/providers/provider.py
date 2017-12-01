'''
A provider base class which defines template for the subtitle sites.
'''
import re
import logging
import requests
import bs4

class ProviderNotSupported(Exception):
    def __init__(self, provider):
        self.provider = provider
        super(ProviderNotSupported, self).__init__(self, 'Provider {} not found.'.format(provider))


class Provider:
    '''
    A base class for providers.
    '''
    def __init__(self, provider_name, base_url, logger_name, lang="EN"):
        self.base_url = base_url
        self.default_lang = lang
        self.logger = logging.getLogger(logger_name)


    def scrape_page(self, url, soup="yes"):
        '''
        Retrieve content from a url.

        Parameters:

        url  :: URL to be scraped
        soup :: Create soup object using bs4 - defaults to 'yes'
        '''
        HEADERS = {'User-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        req = requests.get(url, headers=HEADERS)
        if req.status_code != 200:
            self.logger.debug("{} not retrieved. Status code {} returned.".format(req.url, req.status_code))
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
        url_fed --> https://subscene.com/subtitles/?q= | media name | .
        return --> https://subscene.com/subtitles/?q=media.name
        '''
        return base_url + query.replace(" ", replacor)


    def get_lang(self, provider_name):
        '''
        Get languages for a specific provider.

        Parameters:

        provider_name :: Provider name for subtitle site
        '''
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
        if not provider_name.islower():
            # If provider name is provided in the form of 'Subscene' or
            # 'SUBSCENE', doesn't break.
            provider_name = provider_name.lower()
        if provider_name == 'subscene':
            return PROVIDERS_SUPPORTED_LANGUAGES['subscene']
        elif provider_name == 'allsubdb':
            return PROVIDERS_SUPPORTED_LANGUAGES['allsubdb']
        else:
            raise ProviderNotSupported(provider_name)


    def downloader(self, download_url, filename=""):
        '''
        A downloader method which is used by every provider.

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
