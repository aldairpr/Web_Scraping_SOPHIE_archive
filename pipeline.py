import logging
import subprocess
import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

news_sites_uids = ['Vega']


def main():
    logger.info('Starting process')
    _extract()
    _transform()
    logger.info('Process finished')


def _extract():
    logger.info('Starting extract process')
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    for news_site_uid in news_sites_uids:
        data_filename = '{news_site_uid}_{datetime}.csv'.format(news_site_uid=news_site_uid,datetime=now)
        subprocess.run(['python', 'extract_main.py', news_site_uid], cwd='./extract')
        subprocess.call('mv extract/{} transform'.format(data_filename), shell=True)


def _transform():
    logger.info('Starting transform process')
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = '{news_site_uid}_{datetime}.csv'.format(news_site_uid=news_site_uid,datetime=now)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        subprocess.run(['python', 'transform_main.py', dirty_data_filename], cwd='./transform')
        subprocess.call('mv transform/{} data'.format(clean_data_filename), shell=True)
    subprocess.call('rm transform/*.csv', shell=True)


if __name__ == '__main__':
    main()