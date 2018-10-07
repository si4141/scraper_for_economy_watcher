import unittest
import pandas as pd
import numpy as np
from scraper_for_economy_watchcer.reader import EconomyWatcherReader
import logging
logging.basicConfig()
logging.getLogger("scraper_for_economy_watchcer.reader").setLevel(level=logging.DEBUG)


class TestReader(unittest.TestCase):

    # ----------------
    # normal scenarios
    # ----------------
    def test_getting_data_for_one_month(self):
        reader = EconomyWatcherReader()

        data = reader.get_data('current', pd.datetime(2015,10,1), None)
        # check column names
        self.assertSetEqual(set(data.columns),
                            {'date', 'reason_type', 'industry', 'region', 'is_tokyo', 'field', 'score', 'reason_sentence'})

    def test_getting_data_for_multiple_months(self):
        reader = EconomyWatcherReader()

        data = reader.get_data('current', pd.datetime(2018, 1, 1), pd.datetime(2018,5,1))

        # check data range
        self.assertListEqual(
            list(pd.date_range(pd.datetime(2018, 1, 1), pd.datetime(2018,5,1), freq='MS').values),
            list(np.sort(data.date.unique()))
        )


    def test_getting_all_available_data(self):
        reader = EconomyWatcherReader()
        data = reader.get_data('current')

        date_in_data_str = ['{:%Y%m%d}'.format(date_) for date_ in data.date.unique()]
        self.assertIn('{:%Y%m%d}'.format(reader.EARLIEST_MONTH), date_in_data_str)
        self.assertIn('{:%Y%m%d}'.format(reader.LATEST_MONTH), date_in_data_str)
        self.assertGreater(len(date_in_data_str), 2)

    # --------------------
    # non-normal scenarios
    # --------------------
    def test_raise_exception(self):
        reader = EconomyWatcherReader()

        # invalid `kind_` parameter
        with self.assertRaises(ValueError):
            reader.get_data(kind_= 'invalid', start=pd.datetime(2018, 1, 1))

        # invalid `start` parameter
        with self.assertRaises(ValueError):
            reader.get_data(kind_='current', start=pd.datetime(1945,1,1))

        # invalid `end` parameter
        with self.assertRaises(ValueError):
            reader.get_data(kind_='current', start=pd.datetime(2100, 1, 1))

        # pass `start` > `end`
        with self.assertRaises(ValueError):
            reader.get_data(kind_='current', start=pd.datetime(2018, 1, 1), end=pd.datetime(2017,1,1))


if __name__ == '__main__':
    unittest.main()

