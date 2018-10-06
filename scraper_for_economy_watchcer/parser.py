import numpy as np
import pandas as pd
from settings import TOKYO_FLAG_VALUE_IN_RAW_DATA
from logging import getLogger
logger = getLogger(__name__)


def eliminate_rows_with_na_in_economic_status(watcher_file: pd.DataFrame, iloc_economic_status_score: int):
    logger.info('eliminate rows do not contain economic stats score from data')
    watcher_file = watcher_file[~watcher_file.iloc[:, iloc_economic_status_score].isnull()]
    return watcher_file


def eliminate_newline_code(watcher_file: pd.DataFrame):
    logger.info('eliminate newline code \n and \r from data')
    watcher_file = watcher_file.apply(
        lambda x:x.str.replace('\n', '').str.replace('\r','') if x.dtype == np.object else x
    )
    return watcher_file


def build_is_tokyo_flag(watcher_file: pd.DataFrame, iloc_is_tokyo_flag: int):
    watcher_file = watcher_file.assign(
        is_tokyo=lambda x: ~x.iloc[:, iloc_is_tokyo_flag].isnull() & x.iloc[:, iloc_is_tokyo_flag].str.contains(TOKYO_FLAG_VALUE_IN_RAW_DATA)
    )
    return watcher_file


def make_field_column(watcher_file: pd.DataFrame, iloc_field: int):
    """
    Make field column.
    Fill na value in field column using ffill method in pandas.

    :param watcher_file:
    :param iloc_field:
    :return: DataFrame with field column
    """
    watcher_file = watcher_file.assign(
        field=lambda x: x.iloc[:, iloc_field].fillna(method='ffill')
    )
    return watcher_file


def clean_field_column(watcher_file_with_field: pd.DataFrame):
    """

    :param watcher_file_with_field:
    :return:
    """
    watcher_file_with_field = watcher_file_with_field.assign(
        field=lambda x: x.field.str.replace(r'(\(.*?\))','').str.strip()
    )
    return watcher_file_with_field


def make_region_column(watcher_file: pd.DataFrame, iloc_field: int):
    """
    Make region column from field column.
    Because the value in the field column has region name in parenthesis like `Field Name`(),
    this method extracts string in the parenthesis.
    So, this method might not work if the format of raw data would be changed.

    :param watcher_file:
    :param iloc_field:
    :return:
    """
    watcher_file = watcher_file.assign(
        region=lambda x: x.iloc[:, iloc_field].str.extract(r'((?<=\().*?(?=\)))')
    )
    return watcher_file


def convert_economic_state_score_into_integer(watcher_file: pd.DataFrame, iloc_economic_status_score: int, hash_map_for_score_symbol):
    """
    Convert economic state score into integer.

    :param watcher_file:
    :param iloc_economic_status_score:
    :return:
    """
    def _convert(value):
        try:
            return hash_map_for_score_symbol[value]
        except KeyError:
            return np.nan

    watcher_file = watcher_file.assign(
        score=lambda x: x.iloc[:, iloc_economic_status_score].apply(_convert)
    )
    return watcher_file


def eliminate_rows_without_sentence(watcher_file: pd.DataFrame, iloc_reason_sentence: int):
    """

    :param watcher_file:
    :return:
    """
    watcher_file = watcher_file.dropna(subset=['score'])
    including_sentence = watcher_file.iloc[:, iloc_reason_sentence].apply(lambda x: len(x) > 1)

    return watcher_file[including_sentence]


def clean_sentence_reason(watcher_file: pd.DataFrame, iloc_reason_sentence: int):
    """
    Delete center dot at the head of the sentences.

    :param watcher_file: watcher data, na in the sentence must be eliminated before call this function.
    :param iloc_reason_sentence: index number of reason sentence column
    :return: cleaned date
    """
    watcher_file = watcher_file.assign(
        reason_sentence=lambda x: x.iloc[:, iloc_reason_sentence].str.replace('・', '', n=1)
    )
    return watcher_file
