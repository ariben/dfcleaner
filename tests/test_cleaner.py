# run the below command from the root directory of project
# python3 -m unittest tests.test_cleaner

import unittest
import pandas as pd
import numpy as np
from dfcleaner.cleaner import sanitize, change_dtypes, remove_outliers, fill_nan, preprocess, suggest_convertion_dict


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

    @classmethod
    def tearDownClass(cls):
        print(cls.final_df.info())
        print(cls.final_df)

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
        new_df = self.df.copy()
        new_df.columns = sanitize(self.df.columns)
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
