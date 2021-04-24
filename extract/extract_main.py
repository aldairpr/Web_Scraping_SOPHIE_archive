import argparse
import logging

import datetime
import csv

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

from common import config
import news_page_objects as news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _main(news_site_uid):
    host = config()['SOPHIE_archive'][news_site_uid]['url']
    
    logging.info('Beginning scraper for {}'.format(host))
    logging.info('The uid select if {}'.format(news_site_uid))

    homepage = news.HomePage(news_site_uid, host)

    search_ccf_links, none_url_search_ccf = homepage.search_ccf_links
    view_head_links, none_url_view_head = homepage.view_head_links

    # Join the list of missing urls
    set_url_missing = list(set(none_url_search_ccf + none_url_view_head))

    tablebody = news.TableBody(news_site_uid, host)

    dates = tablebody.date(set_url_missing)
    fibers = tablebody.fiber_b(set_url_missing)
    signal_to_noise = tablebody.signal_to_noise(set_url_missing)

    # get data
    radial_velocity = _get_data_link(news_site_uid, _build_links(search_ccf_links, 'search_ccf'), 'search_ccf')
    julian_day = _get_data_link(news_site_uid, _build_links(view_head_links, 'view_head'), 'view_head')


def _build_links(links, column_name):
    logger.info('Build the links {}'.format(column_name))
    
    join_spaces_links = [link.replace(' ', '') for link in links]
    link_header = 'http://atlas.obs-hp.fr/sophie/'
    
    all_links = []
    for link_body in join_spaces_links:
        all_links.append('{}{}'.format(link_header, link_body))
    return all_links


def _get_data_link(news_site_uid, links, column_name):
    logger.info('Get column data {}'.format(column_name))

    articles_data = []
    for link in links:
        article = _fetch_article(news_site_uid, link, column_name)

        if article:
            #logger.info('Article fetched!!')
            articles_data.append(article)
        
        else:
            articles_data.append(None)
    
    return articles_data

def _fetch_article(news_site_uid, link, column_name):
    #logger.info('Star fetching article ar {}'.format(column_name))

    article = None
    try:
        article = news.HomePage(news_site_uid, link)

    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fechting the article', exc_info=False)
    
    if article and not article.get_html_data(column_name):
        logger.warning('Invalid article. There is no data')
        return None

    return article


if __name__=='__main__':
    parser = argparse.ArgumentParser()

    news_site_choices= list( config()['SOPHIE_archive'].keys() )
    parser.add_argument('SOPHIE_archive',
                        help='The SOPHIE archive that you want to scrape',
                        type=str,
                        choices=news_site_choices)
    args = parser.parse_args()
    _main(args.SOPHIE_archive)
