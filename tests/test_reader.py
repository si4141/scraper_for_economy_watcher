import unittest
import pandas as pd
import numpy as np
from econ_watcher_reader.reader import EconomyWatcherReader
import logging
logging.basicConfig()
logging.getLogger("econ_watcher_reader.reader").setLevel(level=logging.DEBUG)


class TestReaderCurrent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kind_ = 'current'

    # ----------------
    # normal scenarios
    # ----------------
    def test_getting_data_for_one_month(self):
        reader = EconomyWatcherReader()

        data = reader.get_data(self.kind_, pd.datetime(2015,10,1), None)
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

        date_in_data_str = ['{:%Y%m%d}'.format(pd.to_datetime(date_)) for date_ in data.date.unique()]
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


class TestReaderFuture(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kind_ = 'future'

    # ----------------
    # normal scenarios
    # ----------------
    def test_getting_data_for_one_month(self):
        reader = EconomyWatcherReader()

        data = reader.get_data(self.kind_, pd.datetime(2015,10,1), None)
        # check column names
        data.to_clipboard()
        self.assertSetEqual(set(data.columns),
                            {'date', 'industry', 'region', 'is_tokyo', 'field', 'score', 'reason_sentence'})

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

        date_in_data_str = ['{:%Y%m%d}'.format(pd.to_datetime(date_)) for date_ in data.date.unique()]
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

