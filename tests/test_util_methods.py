import unittest
from econ_watcher_reader.settings import TOP_MENU_PAGE, WatcherType, TOKYO_FLAG_VALUE_IN_RAW_DATA
import re
import numpy as np
from econ_watcher_reader.scraper import get_watcher_directory, get_watcher_file,\
    get_publish_date_from_url
import econ_watcher_reader.parser as parser
import logging
logging.basicConfig()
logging.getLogger("econ_watcher_reader").setLevel(level=logging.DEBUG)


class TestScraper(unittest.TestCase):

    def test_get_watcher_directory(self):
        links_ = get_watcher_directory(TOP_MENU_PAGE)
        for link_ in links_:
            self.assertTrue('watcher' in link_)
            self.assertFalse('menu' in link_)
            self.assertTrue(len(re.findall('\d{4}', link_)))

    def test_get_watcher_file(self):
        links_ = get_watcher_directory(TOP_MENU_PAGE)

        data = get_watcher_file(links_[0], WatcherType.Current.file_name)

        self.assertTrue(data.size>0)

    def test_get_publish_date_from_url(self):
        links_ = get_watcher_directory(TOP_MENU_PAGE)
        self.assertIsNotNone(get_publish_date_from_url(links_[0]))


class TestParserCurrent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.links_ = get_watcher_directory(TOP_MENU_PAGE)
        cls.watcher_type = WatcherType.Current
        cls.data = get_watcher_file(cls.links_[0], cls.watcher_type.file_name)

    def test_eliminate_newline_code(self):
        eliminated = parser.eliminate_newline_code(self.data)

        self.assertFalse(eliminated.apply(
            lambda x: x.str.contains('\n').any() if x.dtype == np.object else False
        ).any())
        self.assertFalse(eliminated.apply(
            lambda x: x.str.contains('\r').any() if x.dtype == np.object else False
        ).any())

    def test_eliminate_rows_with_na_in_economic_status(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                      self.watcher_type.iloc_economic_status_score)
        self.assertGreater(eliminated.shape[0], 0)

    def test_build_is_tokyo_flag(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                      self.watcher_type.iloc_economic_status_score)
        flagged = parser.build_is_tokyo_flag(eliminated, self.watcher_type.iloc_is_tokyo_flag)
        self.assertTrue(
            flagged[flagged.is_tokyo].iloc[:, self.watcher_type.iloc_is_tokyo_flag].str.contains(TOKYO_FLAG_VALUE_IN_RAW_DATA).all()
        )

    def test_make_field_column(self):
        eliminated = parser.eliminate_newline_code(self.data)
        eliminated = parser.eliminate_rows_with_na_in_economic_status(eliminated,
                                                                      self.watcher_type.iloc_economic_status_score)

        data_with_field = parser.make_field_column(eliminated, self.watcher_type.iloc_field)

        self.assertFalse(data_with_field.field.isnull().any())

    def test_clean_field_column(self):
        eliminated = parser.eliminate_newline_code(self.data)
        eliminated = parser.eliminate_rows_with_na_in_economic_status(eliminated,
                                                                      self.watcher_type.iloc_economic_status_score)
        data_with_field = parser.make_field_column(eliminated, self.watcher_type.iloc_field)

        cleaned = parser.clean_field_column(data_with_field)
        # TODO assert

    def test_make_region_column(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                     self.watcher_type.iloc_economic_status_score)
        data_with_field = parser.make_field_column(eliminated, self.watcher_type.iloc_field)
        data_with_region = parser.make_region_column(data_with_field)
        # TODO assert

    def test_convert_economic_state_score_into_integer(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                      self.watcher_type.iloc_economic_status_score)
        converted = parser.convert_economic_state_score_into_integer(
            eliminated,
            self.watcher_type.iloc_economic_status_score,
            self.watcher_type.score_map
        )
        self.assertTrue(converted.score.dropna().dtype == np.float)

    def test_eliminate_rows_without_sentence(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                      self.watcher_type.iloc_economic_status_score)
        data_with_integer_score = parser.convert_economic_state_score_into_integer(
            eliminated,
            self.watcher_type.iloc_economic_status_score,
            self.watcher_type.score_map
        )

        eliminated = parser.eliminate_rows_without_sentence(data_with_integer_score,
                                                            self.watcher_type.iloc_reason_sentence)

        self.assertTrue((eliminated.iloc[:, self.watcher_type.iloc_reason_sentence].apply(len) > 1).all())

    def test_clean_sentence_reason(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                     self.watcher_type.iloc_economic_status_score)
        data_with_integer_score = parser.convert_economic_state_score_into_integer(
            eliminated,
            self.watcher_type.iloc_economic_status_score,
            self.watcher_type.score_map
        )

        eliminated = parser.eliminate_rows_without_sentence(data_with_integer_score,
                                                            self.watcher_type.iloc_reason_sentence)

        cleaned = parser.clean_sentence_reason(eliminated, self.watcher_type.iloc_reason_sentence)
        cleaned.to_clipboard()
        # not any values start with center dot `・`
        self.assertFalse((cleaned.reason_sentence.str.find('・') == 0).any())


class TestParserFuture(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.links_ = get_watcher_directory(TOP_MENU_PAGE)
        cls.watcher_type = WatcherType.Future
        cls.data = get_watcher_file(cls.links_[0], cls.watcher_type.file_name)

    def test_eliminate_newline_code(self):
        eliminated = parser.eliminate_newline_code(self.data)

        self.assertFalse(eliminated.apply(
            lambda x: x.str.contains('\n').any() if x.dtype == np.object else False
        ).any())
        self.assertFalse(eliminated.apply(
            lambda x: x.str.contains('\r').any() if x.dtype == np.object else False
        ).any())

    def test_eliminate_rows_with_na_in_economic_status(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                      self.watcher_type.iloc_economic_status_score)
        self.assertGreater(eliminated.shape[0], 0)

    def test_build_is_tokyo_flag(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                      self.watcher_type.iloc_economic_status_score)
        flagged = parser.build_is_tokyo_flag(eliminated, self.watcher_type.iloc_is_tokyo_flag)
        self.assertTrue(
            flagged[flagged.is_tokyo].iloc[:, self.watcher_type.iloc_is_tokyo_flag].str.contains(TOKYO_FLAG_VALUE_IN_RAW_DATA).all()
        )

    def test_make_field_column(self):
        eliminated = parser.eliminate_newline_code(self.data)
        eliminated = parser.eliminate_rows_with_na_in_economic_status(eliminated,
                                                                      self.watcher_type.iloc_economic_status_score)

        data_with_field = parser.make_field_column(eliminated, self.watcher_type.iloc_field)

        self.assertFalse(data_with_field.field.isnull().any())

    def test_clean_field_column(self):
        eliminated = parser.eliminate_newline_code(self.data)
        eliminated = parser.eliminate_rows_with_na_in_economic_status(eliminated,
                                                                      self.watcher_type.iloc_economic_status_score)
        data_with_field = parser.make_field_column(eliminated, self.watcher_type.iloc_field)

        cleaned = parser.clean_field_column(data_with_field)
        # TODO assert

    def test_make_region_column(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                     self.watcher_type.iloc_economic_status_score)
        data_with_field = parser.make_field_column(eliminated, self.watcher_type.iloc_field)
        data_with_region = parser.make_region_column(data_with_field)
        # TODO assert

    def test_convert_economic_state_score_into_integer(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                      self.watcher_type.iloc_economic_status_score)
        converted = parser.convert_economic_state_score_into_integer(
            eliminated,
            self.watcher_type.iloc_economic_status_score,
            self.watcher_type.score_map
        )
        self.assertTrue(converted.score.dropna().dtype == np.float)

    def test_eliminate_rows_without_sentence(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                      self.watcher_type.iloc_economic_status_score)
        data_with_integer_score = parser.convert_economic_state_score_into_integer(
            eliminated,
            self.watcher_type.iloc_economic_status_score,
            self.watcher_type.score_map
        )

        eliminated = parser.eliminate_rows_without_sentence(data_with_integer_score,
                                                            self.watcher_type.iloc_reason_sentence)

        self.assertTrue((eliminated.iloc[:, self.watcher_type.iloc_reason_sentence].apply(len) > 1).all())

    def test_clean_sentence_reason(self):
        eliminated = parser.eliminate_rows_with_na_in_economic_status(self.data,
                                                                     self.watcher_type.iloc_economic_status_score)
        data_with_integer_score = parser.convert_economic_state_score_into_integer(
            eliminated,
            self.watcher_type.iloc_economic_status_score,
            self.watcher_type.score_map
        )

        eliminated = parser.eliminate_rows_without_sentence(data_with_integer_score,
                                                            self.watcher_type.iloc_reason_sentence)

        cleaned = parser.clean_sentence_reason(eliminated, self.watcher_type.iloc_reason_sentence)
        # not any values start with center dot `・`
        self.assertFalse((cleaned.reason_sentence.str.find('・') == 0).any())


if __name__ == '__main__':
    unittest.main()
