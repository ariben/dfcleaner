# run the below command from the root directory of project
# python3 -m unittest tests.test_cleaner

import unittest
import pandas as pd
import numpy as np
from dfcleaner.cleaner import sanitize, change_dtypes, remove_outliers, fill_nan, preprocess, suggest_convertion_dict, spot_irrelevant_columns


class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        self.sanitize_arr = [
            "having_IP_Address",
            "URL_Length",
            "Shortining_Service",
            "having_At_Symbol",
            "double_slash_redirecting",
            "Prefix_Suffix",
            "having_Sub_Domain",
            "domain_registeration_length",
            "Favicon",
            "port",
            "HTTPS_token",
            "Request_URL",
            "URL_of_Anchor",
            "Links_in_tags",
            "SFH",
            "Submitting_to_email",
            "Abnormal_URL",
            "Redirect",
            "on_mouseover",
            "RightClick",
            "popUpWidnow",
            "Iframe",
            "age_of_domain",
            "DNSRecord",
            "web_traffic",
            "Page_Rank",
            "Google_Index",
            "Links_pointing_to_page",
            "Statistical_report",
            "Result",
            "  485_5468a44  _44   4 ?  $@e3   *   C cc    c D  ",
        ]

        self.sample_col_names = [
            'first name',
            'First_Name',
            'first_name',
            'firstname',
            'surname',
            'Surname',
            'SurName',
            'namek',
            'rfid',
            'idea',
            'id',
            'Id',
            'iD',
            'ID',
            'customer_id',
            'customer id',
        ]

        self.df_change_dtypes = pd.DataFrame({
            'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'b': [1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'c': [1, '2', 3, 4, 5, 6, '7', 8, 9, 10, '11', 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'd': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
            'e': [1, 2, 3, 4, '?', '?', 7, 8, 9, 10, 11, '?', 13, 14, 15, 16, 17, '?', 19, 20],
            'f': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'],
            'g': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        })

        self.df_outlier_regression = pd.DataFrame({
            'a': [1, 2, 9000, 4, 5, 6],
            'label': [42, 58, 62, 47, 13, 75],
        })
        self.df_outlier_classification = pd.DataFrame({
            'a': [5, 10, 7, 19, -99999, 17],
            'label': [1, 0, 0, 0, 1, 0],
        })

        self.df_fill_nan = pd.DataFrame({
            'a': [1, 2, 3, 4, 5, 6],
            'b': [np.nan, 2, 3, 4, np.nan, 6],
        })

        self.df_suggest_convertion = pd.DataFrame({
            'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'b': ['1', np.nan, '3', '4', '5', 6, '7', '8', 9, '10', '11'],
            'c': ['?', '2', 3, 4, 5, 6, 7, 8, 9, 10, 11],
        })

    def test_sanitize(self):
        new_cols = sanitize(self.sanitize_arr)

        self.assertListEqual(
            new_cols,
            [
                "having_ip_address",
                "url_length",
                "shortining_service",
                "having_at_symbol",
                "double_slash_redirecting",
                "prefix_suffix",
                "having_sub_domain",
                "domain_registeration_length",
                "favicon",
                "port",
                "https_token",
                "request_url",
                "url_of_anchor",
                "links_in_tags",
                "sfh",
                "submitting_to_email",
                "abnormal_url",
                "redirect",
                "on_mouseover",
                "right_click",
                "pop_up_widnow",
                "iframe",
                "age_of_domain",
                "dns_record",
                "web_traffic",
                "page_rank",
                "google_index",
                "links_pointing_to_page",
                "statistical_report",
                "result",
                "485_5468a44_44_4_e3_c_cc_c_d",
            ]
        )

    def test_change_dtypes(self):
        self.df_change_dtypes = change_dtypes(
            self.df_change_dtypes,
            {
                'a': 'float',
                'b': int,
                'c': 'int',
                'd': int,
                'e': float,
                'g': 'category',
            }
        )

        self.assertEqual(self.df_change_dtypes['a'].dtype, float)
        self.assertEqual(self.df_change_dtypes['b'].dtype, 'int')
        self.assertEqual(self.df_change_dtypes['c'].dtype, 'int')
        self.assertEqual(self.df_change_dtypes['d'].dtype, int)
        self.assertEqual(self.df_change_dtypes['e'].dtype, float)
        self.assertEqual(self.df_change_dtypes['g'].dtype, 'category')

    def test_remove_outliers(self):
        self.df_outlier_regression = remove_outliers(self.df_outlier_regression,
                                                     label_col='label',
                                                     std_coeff=1.5)
        self.df_outlier_classification = remove_outliers(self.df_outlier_classification,
                                                         label_col='label',
                                                         std_coeff=1.5)

        np.testing.assert_array_equal(list(self.df_outlier_regression['a']),
                                      [1.0, 2.0, np.nan, 4.0, 5.0, 6.0])
        np.testing.assert_array_equal(list(self.df_outlier_classification['a']),
                                      [5, 10, 7, 19, np.nan, 17])

    def test_fill_nan(self):
        self.df_fill_nan = fill_nan(self.df_fill_nan, 'mean')
        self.assertListEqual(list(self.df_fill_nan['a']),
                             [1, 2, 3, 4, 5, 6])
        self.assertListEqual(list(self.df_fill_nan['b']),
                             [3.75, 2, 3, 4, 3.75, 6])

        # the above test fills the null values in numeric columns of df
        # with mean. Therefore, reset the df back to original
        # to test for filling null values with median
        self.setUp()

        self.df_fill_nan = fill_nan(self.df_fill_nan, 'median')
        self.assertListEqual(list(self.df_fill_nan['a']),
                             [1, 2, 3, 4, 5, 6])
        self.assertListEqual(list(self.df_fill_nan['b']),
                             [3.5, 2, 3, 4, 3.5, 6])

        with self.assertRaises(ValueError):
            fill_nan(self.df_fill_nan, 'asdf')
            fill_nan(self.df_fill_nan, 5.0)

    def test_suggest_convertion_dict(self):
        suggested_convertion_dict = suggest_convertion_dict(
            self.df_suggest_convertion)
        self.assertEqual(suggested_convertion_dict, {'b': float, 'c': float})

    def test_suggest_col_drop(self):
        cols_to_drop = spot_irrelevant_columns(self.sample_col_names)

        self.assertListEqual(
            cols_to_drop,
            [
                'first name',
                'First_Name',
                'first_name',
                'firstname',
                'surname',
                'Surname',
                'SurName',
                'id',
                'Id',
                'iD',
                'ID',
                'customer_id',
                'customer id',
            ]
        )

        # if __name__ == "__main__":
        #     unittest.main()
