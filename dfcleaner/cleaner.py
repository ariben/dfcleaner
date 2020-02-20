import pandas as pd
import numpy as np
import re


def preprocess(df, column_dtype_conversion_dictionary={}, std_coeff=1.5, fill_na_method='median', label_col=None):
    '''
    A convinient function that 
        - changes the datatypes of columns according to the 
            values given in the 'column_dtype_conversion_dictionary'
            argument
        - drops duplicate rows
        - if there is a target(label) column then drops all rows where that
            column value is null
        - removes outliers according to the std coefficient given as a parameter
            (doesn't consider the target(label) column to check for outliers)
        - fills nan values according to the fill_na_method parameter

    Note: This function performs all the above said actions in the 
        same order as mentioned.

    All the functions that are used here can also be used
    independently.

    Returns: 
        A cleaned up dataframe

    Args:
        df: pandas.DataFrame object

        column_dtype_conversion_dictionary: dictionary having keys as the 
            column name and value as the desired dtype

        std_coeff: coefficient of standard deviation in outlier removal

        fill_na_method: 'mean' or 'median'. nan values of each column will
            be replaced by that column's mean or median

        label_col: the target(label) column name (if any) as a string
    '''
    # df = sanitize_column_names(df)
    df = change_dtypes(df, column_dtype_conversion_dictionary)
    df = df.drop_duplicates()

    if label_col is not None:
        df = df.dropna(subset=[label_col])

    df = remove_outliers(df, std_coeff, label_col=label_col)
    df = fill_nan(df, fill_na_method, label_col=label_col)

    return df


def sanitize(arr):
    '''
    for each string in the array, this function will
        - keeps only alphanumeric, space and underscore characters
        - replaces multiple consecutive spaces with a single space
        - strips leading and trailing white spaces
        - replace spaces with underscores
        - convert CamelCase to snake_case
        - remove multiple consecutive underscores again
        - convert the whole string into lowercase

    Note: This function performs all the above said actions in the 
        same order as mentioned

    Returns: array of strings where the strings are 'sanitized'
    Args:
        arr: array of strings
    '''
    new_arr = []
    for string in arr:
        # only keep alphanumeric, space and underscore
        string = re.sub(r"[^A-Za-z0-9 _]", "", string)

        # remove multiple consecutive spaces
        string = re.sub(r" +", " ", string)

        # strip leading and trailing white spaces, lowercase
        # and replace space with underscore
        string = string.strip().replace(" ", "_")

        # convert CamelCase to snake_case
        string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        string = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string)

        # remove multiple consecutive underscores
        string = re.sub(r"_+", "_", string)

        # lower case
        string = string.lower()
        new_arr.append(string)

    return new_arr


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
    '''
    This function will take a pandas.DataFrame and a 
    conversion dictionary as input and changes the datatypes 
    of the columns according to the conversion dictionary.

    Usage scenario 1:
        If a column where the values are like '$25.99', '$ 7.2', '$29,347.32' ...
        where you want to extract the float number and leave the string characters like '$', ',', ' ' ...
        you can just include the column name as key and float as value in the conversion dictionary
            Eg: {'col_name': float}

    Usage scenario 2:
        If a column where the values are actually float but because 
        of a single string character somewhere, the whole dtype 
        changes to Object
            Eg: a column has these values 27.6, 48.125, 24, ?, 74.32

        The ? is a string character in a numeric column trying to represent nan value
        In this case, simply include the key value pairs in the conversion dict 
        {'col_name': float}

    Returns: pandas.DataFrame with the changed datatypes

    Args:
        df: pandas.DataFrame object
        conversion_dict: dictionary with column names as keys and the 
            dtypes as values
            Eg: {'col_0': float, 'col_1': 'category', 'col_5': int}
    '''
    for col_name, dtype in conversion_dictionary.items():
        if dtype in [int, float]:
            if df[col_name].dtype not in [int, float]:
                df[col_name] = df[col_name].apply(
                    lambda x: _filter_characters(dtype, x))
            else:
                df[col_name] = df[col_name].astype(dtype)

        else:
            df[col_name] = df[col_name].astype(dtype)

    return df


def remove_outliers(df, std_coeff=1.5, label_col=None):
    '''
    This function will take a dataframe and replaces all the outliers
    with np.nan.
    If target(label) column name is given, then it wont consider that
    column to check and remove outliers.

    The outliers are determined based on the std_coeff given as a parameter.

    Returns: pandas.DataFrame object without outlier values
    Args:
        df: pandas.DataFrame object
        std_coeff: the coefficient of standard deviation
            Eg: 1.5(recommended) or 3
        label_col: the target(label) column name (if any) as a string

    '''
    cols = list(df.columns)

    # consider only feat cols while removing outliers
    if label_col is not None:
        cols.remove(label_col)

    for col_name in cols:
        if df[col_name].dtype in [int, float]:
            df[col_name] = df[col_name].mask(df[col_name].sub(
                df[col_name].mean()).div(df[col_name].std()).abs().gt(std_coeff))

    return df


def fill_nan(df, how, label_col=None):
    '''
    This function will take a pandas.DataFrame and fills all the 
    null values in all columns according to the method provided.

    If target(label) column name is given, then it wont consider that
    column to fill null values.

    Returns: pandas.DataFrame object without any null values

    Args:
        df: pandas.DataFrame
        how: 'median'(recommended) or 'mean'
        label_col: the target(label) column name (if any) as a string
    '''
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


def suggest_conversion_dict(df):
    # use the _can_convert_to_float() function
    # if the column has nan then definitely int dtype
    '''
    This function checks if any string columns can be converted into float
    Eg:
        - a column may have numeric values but in string format 
            like, '12.0', '15.7'.
        - a column may have special symbols or characters instead 
            of np.nan, like, '?', 'null', 'na' along with normal 
            numbers like 12, 14.26, 85.15, ...
        - because of a single string value, the whole column might 
            have the 'Object' or 'category' datatype

    This function also checks if any numeric (int or float) columns can be converted into categorical columns with the dtype 'category'.
    Eg:
        - a column namely has_credit_card may have binary values 1 or 0.
        - This column can be considered as categorical because the 
            ratio of the number of unique values in the column to 
            the total number of values in the column is very small 
            (smaller than a threshold of 0.01)

    returns: dictionary that can be passed as an argument to the change_dtypes() function

    Args:
        df: pandas.DataFrame
    '''

    suggested_conversion_dict = {}
    for col in df.columns:
        if df[col].dtype in [int, float]:
            if _can_convert_to_category(df[col]):
                suggested_conversion_dict[col] = 'category'

        else:
            if _can_convert_to_float(df[col]):
                suggested_conversion_dict[col] = float

    return suggested_conversion_dict


def _can_convert_to_category(feat_col, threshold=0.01):
    '''
    determine if a numeric column is actually categorical by
    looking at what percentage of unique values are there when
    compared to the total number values
    Eg: 'has_credit_card' might have values 1 or 0
        which is technically numeric(int) but actually categorical
    '''
    uniq_len = len(feat_col.unique())
    total_len = len(feat_col)

    if uniq_len / total_len < threshold:
        return True

    return False


def spot_irrelevant_columns(cols):
    '''
    if there are any columns like names, first_names, ID
    then they are suggested to be dropped

    Args:
        cols: a list of column names

    returns:
        a list of columns to drop
    '''
    cols_to_drop = []
    for col in cols:
        if re.search(r'name\b', col.lower()):
            cols_to_drop.append(col)
        if re.search(r'(\b|[ _])id\b', col.lower()):
            cols_to_drop.append(col)

    return cols_to_drop
