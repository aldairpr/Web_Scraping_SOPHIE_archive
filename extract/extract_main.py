import argparse
import logging

import datetime
import csv

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

from common import config
import sophie_archive_objects as sophie

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _main(sophie_site_uid):
    host = config()['SOPHIE_archive'][sophie_site_uid]['url']
    
    logging.info('Beginning scraper for {}'.format(host))
    logging.info('The uid select if {}'.format(sophie_site_uid))

    homepage = sophie.HomePage(sophie_site_uid, host)

    search_ccf_links, none_url_search_ccf = homepage.get_links('search_ccf')
    view_head_links, none_url_view_head = homepage.get_links('view_head')

    # Join the list of missing urls
    set_url_missing = list(set(none_url_search_ccf + none_url_view_head))

    # Get data from dates, fibers, signal_to_noise
    tablebody = sophie.TableBody(sophie_site_uid, host)

    dates = tablebody.get_tablebody_data('date', set_url_missing)
    fibers = tablebody.get_tablebody_data('fiber_b', set_url_missing)
    signal_to_noise = tablebody.get_tablebody_data('sn26', set_url_missing)

    # Get html from radial_velocity, julian_day
    html_search_ccf = _get_html(sophie_site_uid, _build_links(search_ccf_links, 'search_ccf'), 'search_ccf')
    html_view_head = _get_html(sophie_site_uid, _build_links(view_head_links, 'view_head'), 'view_head')

    # Get data from radial_velocity, julian_day
    radial_velocity = get_data_RV(html_search_ccf, 'search_ccf')
    julian_day = get_data_JD(html_view_head, 'view_head')
    
    # List of elements that will be in the CSV file
    all_data = [dates, fibers, signal_to_noise, radial_velocity, julian_day]
    all_header = ['dates', 'fibers', 'signal_to_noise', 'radial_velocity', 'julian_day']
    
    return _save_articles(sophie_site_uid, all_data, all_header)


def _build_links(links, column_name):
    logger.info('Build the links {}'.format(column_name))
    
    join_spaces_links = [link.replace(' ', '') for link in links]
    link_header = 'http://atlas.obs-hp.fr/sophie/'
    
    all_links = []
    for link_body in join_spaces_links:
        all_links.append('{}{}'.format(link_header, link_body))
    return all_links


def _get_html(sophie_site_uid, links, column_name):
    logger.info('Get column data {}'.format(column_name))

    articles_data = []
    for link in links:
        article = _fetch_article(sophie_site_uid, link, column_name)

        if article:
            #logger.info('Article fetched!!')
            articles_data.append(article)
    
    return articles_data

def _fetch_article(sophie_site_uid, link, column_name):
    #logger.info('Star fetching article of {}'.format(column_name))
    #logger.info('link: {}'.format(link))

    article = None
    try:
        article = sophie.HomePage(sophie_site_uid, link)

    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fechting the article', exc_info=False)
    
    if article and not article.get_html_link(column_name):
        logger.warning('Invalid article. There is no data')
        return None

    return article


def get_data_RV(html_view_head, column_name):
    logger.info('Get data RV')
    rv = []
    for html in html_view_head:
        if len(html.radial_velocity()) != 0:
            rv.append( html.radial_velocity() )
        elif len(html.radial_velocity()) == 0:
            rv.append( '' )
    return rv

def get_data_JD(html_view_head, column_name):
    logger.info('Get data JD')
    JD = []
    for html in html_view_head:
        if len(html.julian_day()) != 0:
            JD.append( html.julian_day() )
        elif len(html.julian_day()) == 0:
            JD.append( '' )
    return JD


def _save_articles(sophie_site_uid, all_data, all_header):
    logger.info('Create dataframe of {}'.format(sophie_site_uid))
    
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{sophie_site_uid}_{datetime}.csv'.format(
                    sophie_site_uid=sophie_site_uid,
                    datetime=now)
    
    df = pd.DataFrame(all_data).T
    df.columns = all_header

    return df.to_csv(out_file_name, index = False, sep=';')


if __name__=='__main__':
    parser = argparse.ArgumentParser()

    sophie_site_choices= list( config()['SOPHIE_archive'].keys() )
    parser.add_argument('SOPHIE_archive',
                        help='The SOPHIE archive that you want to scrape',
                        type=str,
                        choices=sophie_site_choices)
    args = parser.parse_args()
    _main(args.SOPHIE_archive)
