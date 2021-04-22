import bs4
import requests

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

    
    # Opcional
    def _get_headers(self):
        row_header = self._select(self._queries['header'])
        # header de table_body
        header = []
        for i in range(0, len(row_header)):
            header.append(row_header[i].text)
        
        # Lista de datos que deseo obtener
        lista = ['date', 'fiber_b', 'sn26', 'view_spec', 'search_ccf']  
        position = []
        for i in range(0, len(header)):
            for j in range(0, len(lista)):
                if header[i] == lista[j]:
                    position.append(i)

        columns = {}
        for i in range(0, len(lista)):
            columns[lista[i]] = position[i]
        return columns
    

    def _get_rows(self):
        return self._select(self._queries['rows'])

    
class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)


    def _obtein_link(self, column_name):
        rows = self._get_rows()
        position_column = self._get_headers()[column_name]
    
        select_a = []
        for i in range(0, len(rows)):
            data = rows[i].select('td')[position_column].select('a')
            select_a.append(data)
        
        link_list = []
        none_url = []
        for index, link in enumerate(select_a):
            if len(link) ==0:
                link = [None]
                none_url.append(index)
            if link[0] and link[0].has_attr('href'):
                link_list.append(link)
         
        return list(set(link[0]['href'] for link in link_list)), none_url

    
    @property
    def serch_CCF_links(self):
        return self._obtein_link('search_ccf')

    @property
    def view_spec_links(self):
        return self._obtein_link('view_spec')




    


class TableBody(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
    

    def _obtein_data(self, column_name):
        rows = self._get_rows()
        position_column = self._get_headers()[column_name]

        results = []
        for i in range(0, len(rows)):
            data = rows[i].select('td')[position_column].text
            if len(data) !=0:
                results.append(data)
            elif len(data) == 0:
                results.append('')
        return results
    

    @property
    def date(self):
        return self._obtein_data('date')
    
    @property
    def fiber_b(self):
        return self._obtein_data('fiber_b')
    
    @property
    def signal_to_noise(self):
        return self._obtein_data('sn26')




