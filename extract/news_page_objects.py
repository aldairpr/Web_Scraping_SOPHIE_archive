import bs4
import requests
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from common import config

class NewsPage:

    def __init__(self, news_site_uid, url):
        # Rama principal con el html
        self._config = config()['SOPHIE_archive'][news_site_uid]
        self._queries = self._config['table_body']
        self._html = None
        self._url = url

        self._visit(url)

    # hacer select del html de news_site_uid
    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

    def _get_headers(self):
        row_header = self._select(self._queries['header'])
        # table_body's header
        headers = [header.text for header in row_header]

        # List of data I want to get
        data_list = ['date', 'fiber_b', 'sn26', 'view_head', 'search_ccf']  
        data_position = []
        for i in range(0, len(headers)):
            for data in data_list:
                if headers[i] == data:
                    data_position.append(i)

        column_header = {}
        for i in range(0, len(data_list)):
            column_header[data_list[i]] = data_position[i]
        return column_header
    
    def _get_rows(self):
        return self._select(self._queries['rows'])

    
class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    def _obtein_link(self, column_name):
        logger.info('Get links of {}'.format(column_name))

        rows = self._get_rows()
        position_column = self._get_headers()[column_name]
    
        select_a = []
        for row in rows:
            data = row.select('td')[position_column].select('a')
            select_a.append(data)
        
        link_list = []
        none_url_list = []
        for index, link in enumerate(select_a):
            if len(link) == 0:
                none_url_list.append(index)
            elif link[0] and link[0].has_attr('href'):
                link_list.append(link)
         
        return list(link[0]['href'] for link in link_list), none_url_list

    @property
    def search_ccf_links(self):
        return self._obtein_link('search_ccf')

    @property
    def view_head_links(self):
        return self._obtein_link('view_head')

    def get_html_data(self, column_name):
        return self._select(self._queries[column_name])



class TableBody(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
    
    def _obtein_data(self, column_name, set_url_missing):
        logger.info('Get data of {}'.format(column_name))

        rows = self._get_rows()
        position_column = self._get_headers()[column_name]

        results = []
        for row in rows:
            data = row.select('td')[position_column].text
            if len(data) !=0:
                results.append(data)
            elif len(data) == 0:
                results.append('')
        
        clean_results = np.delete(results, set_url_missing).tolist() 
        return clean_results
    
    def date(self, set_url_missing):
        return self._obtein_data('date', set_url_missing)
    
    def fiber_b(self, set_url_missing):
        return self._obtein_data('fiber_b', set_url_missing)
    
    def signal_to_noise(self, set_url_missing):
        return self._obtein_data('sn26', set_url_missing)

