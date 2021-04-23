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

    serch_CCF_links, none_url_serch_CCF = homepage.serch_CCF_links
    view_head_links, none_url_view_head = homepage.view_head_links

    # Join the list of missing urls
    set_url_missing = list(set(none_url_serch_CCF + none_url_view_head))

    tablebody = news.TableBody(news_site_uid, host)

    dates = tablebody.date(set_url_missing)
    fibers = tablebody.fiber_b(set_url_missing)
    sns = tablebody.signal_to_noise(set_url_missing)

    print('serch_CCF_links ',len(serch_CCF_links))
    print('view_head_links ',len(view_head_links))
    print('dates ',len(dates))
    print('fibers ',len(fibers))
    print('sns ',len(sns))



if __name__=='__main__':
    parser = argparse.ArgumentParser()

    news_site_choices= list( config()['SOPHIE_archive'].keys() )
    parser.add_argument('SOPHIE_archive',
                        help='The SOPHIE archive that you want to scrape',
                        type=str,
                        choices=news_site_choices)
    args = parser.parse_args()
    _main(args.SOPHIE_archive)
