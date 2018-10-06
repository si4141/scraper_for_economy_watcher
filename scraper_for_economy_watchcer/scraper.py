import requests
from settings import WATCHER_DISTRIBUTE_DIRECTORY, DATA_STORE, TOP_MENU_PAGE, WatcherType
from bs4 import BeautifulSoup
from enum import Enum
import numpy as np
import pandas as pd
import os.path
import re
from typing import List
import datetime
from logging import getLogger
logger = getLogger(__name__)


def _get_watcher_directory(menu_page: str):
    response = requests.get(menu_page)

    logger.info('get watcher links from %s' % response.url)

    soup = BeautifulSoup(response.content, features="html.parser")
    links_ = soup.find_all('a', class_='bulletLink')
    links_ = [os.path.dirname(link_.get('href')) + '/' for link_ in links_ if 'menu' in link_.get('href')]

    logger.info('done')
    return links_


def _get_watcher_file(link_: str, file_name: str):
    file_url = WATCHER_DISTRIBUTE_DIRECTORY + link_ + file_name

    logger.info('get watcher file from %s' % file_url)

    data = pd.read_csv(file_url, header=None, encoding='cp932')
    return data


def _get_publish_date_from_url(link_: str) -> datetime.datetime:
    logger.info('get publish date from url.')
    yyyymmdd = ''.join(re.findall(r'\d{4}', link_))
    pub_date = datetime.datetime.strptime(yyyymmdd, '%Y%m%d')

    logger.debug('yyyymmdd: {0}, date: {1:}'.format(*[yyyymmdd, pub_date]))
    return pub_date


def _eliminate_rows_with_na_in_economic_status(watcher_file: pd.DataFrame, iloc_economic_status_score: int):
    logger.info('eliminate rows do not contain economic stats score from data')
    watcher_file = watcher_file[~watcher_file.iloc[:, iloc_economic_status_score].isnull()]
    return watcher_file


def _eliminate_newline_code(watcher_file: pd.DataFrame):
    logger.info('eliminate newline code \n and \r from data')
    watcher_file = watcher_file.apply(lambda x:x.str.replace('¥n', '').str.replace('¥r','')
                                                    if x.dtype == np.object else x)
    return watcher_file


