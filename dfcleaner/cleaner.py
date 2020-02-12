import pandas as pd
import numpy as np
import re


def preprocess(df, column_dtype_conversion_dictionary, std_coeff, fill_na_method):
    '''
    Args:
        column_dtype_conversion_dictionary: dictionary having keys as the 
            column name and value as the desired dtype

        std_coeff: coefficient of standard deviation in outlier removal

        fill_na_method: 'mean' or 'median'. nan values of each column will
            be replaced by that column's mean or median
    '''
    # df = sanitize_column_names(df)
    df = change_dtypes(df, column_dtype_conversion_dictionary)
    df = df.drop_duplicates()
    df = remove_outliers(df, std_coeff)
    df = fill_nan(df, fill_na_method)

    return df


def sanitize_column_names(df):
    '''
    changes the column names to lowercase, strips any leading and trailing white space,
    replaces space between words to underscores and only keeps alphanumeric (and underscore) 
    characters
    '''
    new_cols = []
    for col in df.columns:
        # only keep alphanumeric and space
        col = re.sub(r"[^A-Za-z0-9 ]", "", col)
        # remove multiple consecutive spaces
        col = re.sub(r" +", " ", col)
        # strip leading and trailing white spaces, lowercase
        # and replace space with underscore
        col = col.strip().lower().replace(" ", "_")
        new_cols.append(col)

    df.columns = new_cols
    return df


def _filter_characters(dtype, element):
    '''
    if input element is not string then just returns the same element
    else,
    allows only digits and '.' and rejects other characters from
    given string

    Args:
        dtype: the desired dtype to convert the element into

    Example:
        input: "$ 5,000.00" (element is string therefore process it)
        output: 5000.00

        input: np.nan
        output: np.nan (returns the same element because element is not string)

        input: -6
        output: -6 (returns the same element because element is not string)

    '''
    if type(element) != str:
        return element
    else:
        filtered_characters = []
        for char in element:
            if char.isdigit() or char == '.':
                filtered_characters.append(char)

        if len(filtered_characters) == 0:
            return np.nan
        return dtype(''.join(filtered_characters))


def change_dtypes(df, conversion_dictionary):
    ''' first applies the functions then changes the dtypes '''
    for col_name, dtype in conversion_dictionary.items():
        if dtype in [int, float]:
            df[col_name] = df[col_name].apply(
                lambda x: _filter_characters(dtype, x))

        else:
            df[col_name] = df[col_name].astype({col_name: dtype})

    return df


def remove_outliers(df, std_coeff):
    for col_name in df.columns:
        if df[col_name].dtype in [int, float]:
            df[col_name] = df[col_name].mask(df[col_name].sub(
                df[col_name].mean()).div(df[col_name].std()).abs().gt(std_coeff))

    return df


def fill_nan(df, how):
    for col_name in df.columns:
        if df[col_name].dtype in [int, float]:
            if how == "median":
                df[col_name] = df[col_name].fillna(df[col_name].median())
            elif how == "mean":
                df[col_name] = df[col_name].fillna(df[col_name].mean())
            else:
                raise ValueError("'how' parameter must be 'mean' or 'median'")

    return df


def _can_convert_to_float(feat_col):
    '''
    determine if a feature column need to change their dtype from
    string to float by picking 10 random samples from that
    column and trying to parse it as float (float(value)).
    If the majority of them get converted to float then the
    dtype may be converted to float.
    eg: a numeric column might have a '?' instead of np.nan

    Args:
        feat_col: pandas.Series object (dataframe column)
    '''
    num_samples = 10
    required_sucess_ratio = 2/3
    samples = feat_col.sample(num_samples)

    successful_parse_count = 0
    for sample in samples:
        try:
            float(sample)
            successful_parse_count += 1
        except ValueError:
            pass

    if successful_parse_count > num_samples*required_sucess_ratio:
        return True
    return False


def suggest_convertion_dict(df):
    # use the _can_convert_to_float() function
    # if the column has nan then definitely int dtype
    '''
    this function focuses mainly on the string columns and
    checks if they can be converted into float
    Eg: a column may have numeric values but in string format
        like, '12.0', '15.7', ....

        or, a column may have special symbols or characters instead
        of np.nan, like, '?', 'null', 'na' along with normal numbers 
        like 12, 14.26, 85.15, .....

        because of a single string value, the whole column might have
        the 'object' or 'category' datatype

    returns:
        conversion dictionary that can be passed as an augument
        to the preprocess() function
    '''

    suggested_convertion_dict = {}
    for col in df.columns:
        if df[col].dtype not in [int, float] and _can_convert_to_float(df[col]):
            suggested_convertion_dict[col] = float

    return suggested_convertion_dict
