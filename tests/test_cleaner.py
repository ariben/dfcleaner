# run the below command from the root directory of project
# python3 -m unittest tests.test_cleaner

import unittest
import pandas as pd
import numpy as np
from dfcleaner.cleaner import sanitize_column_names, change_dtypes, remove_outliers, fill_nan, preprocess, suggest_convertion_dict


class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.df = pd.DataFrame({"A": [1, np.nan, 3, 4, 5, 50], "b": ["$ 50.0", "$2,000.00", -1.0, 0.0, np.nan, 6.0],
                                "  485_5468a44  _44   4 ?  $@e3   *   C cc    c D  ": ["z", np.nan, "asd", "?wa\n kk  a", "3456", "$%^&*"]})

        self.df2 = pd.DataFrame({
            'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'b': ['1', np.nan, '3', '4', '5', 6, '7', '8', 9, '10', '11'],
            'c': ['?', '2', 3, 4, 5, 6, 7, 8, 9, 10, 11],
        })

        self.df_sanitize_column_names = pd.DataFrame(
            {
                "having_IP_Address": [1],
                "URL_Length": [1],
                "Shortining_Service": [1],
                "having_At_Symbol": [1],
                "double_slash_redirecting": [1],
                "Prefix_Suffix": [1],
                "having_Sub_Domain": [1],
                "domain_registeration_length": [1],
                "Favicon": [1],
                "port": [1],
                "HTTPS_token": [1],
                "Request_URL": [1],
                "URL_of_Anchor": [1],
                "Links_in_tags": [1],
                "SFH": [1],
                "Submitting_to_email": [1],
                "Abnormal_URL": [1],
                "Redirect": [1],
                "on_mouseover": [1],
                "RightClick": [1],
                "popUpWidnow": [1],
                "Iframe": [1],
                "age_of_domain": [1],
                "DNSRecord": [1],
                "web_traffic": [1],
                "Page_Rank": [1],
                "Google_Index": [1],
                "Links_pointing_to_page": [1],
                "Statistical_report": [1],
                "Result": [1],
                "  485_5468a44  _44   4 ?  $@e3   *   C cc    c D  ": [1],
            }
        )

    @classmethod
    def tearDownClass(cls):
        print(cls.final_df.info())
        print(cls.final_df)

    def test_sanitize_column_names(self):
        new_df = sanitize_column_names(self.df_sanitize_column_names)
        new_cols = list(new_df.columns)

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
        new_df = change_dtypes(self.df, {"b": float})

        self.assertEqual(new_df["b"].dtype, float)

    # def test_remove_outliers(self):
    #     new_df = remove_outliers(self.df, 1.5)

    def test_fill_nan(self):
        new_df = fill_nan(self.df, 'mean')
        self.assertEqual(list(new_df["A"]), [
                         1.0, 12.6, 3.0, 4.0, 5.0, 50.0])

        # the above test fills the null values in numeric columns of df
        # with mean. Therefore, reset the df back to original
        # to test for filling null values with median
        self.setUp()

        new_df = fill_nan(self.df, 'median')
        self.assertEqual(list(new_df["A"]), [
                         1.0, 4.0, 3.0, 4.0, 5.0, 50.0])

        with self.assertRaises(ValueError):
            fill_nan(self.df, 'asdf')
            fill_nan(self.df, 5.0)

    def test_preprocess(self):
        new_df = sanitize_column_names(self.df)
        new_df = preprocess(new_df, {"a": int, "b": float, "485_5468a44_44_4_e3_c_cc_c_d": 'category'},
                            1.5, 'median')

        # made it a class attribute inorder to use it in the
        # tearDownClass (to print the df and its info)
        self.__class__.final_df = new_df

    def test_suggest_convertion_dict(self):
        suggested_convertion_dict = suggest_convertion_dict(self.df2)
        self.assertEqual(suggested_convertion_dict, {'b': float, 'c': float})

# if __name__ == "__main__":
#     unittest.main()
