import pandas as pd
import os


def change_logger(enable_logging, log_dir=''):
    def decorator(function):
        if not enable_logging:
            return function

        def wrapper(df, *args, **kwargs):
            old_df = df.copy(deep=True)
            df = function(df, *args, **kwargs)

            change_df = _df_diff(old_df, df)

            log_filepath = os.path.join(log_dir,
                                        '{}_log.csv'.format(function.__name__))

            change_df.to_csv(log_filepath)

            return df
        return wrapper
    return decorator


def _df_diff(oldFrame, newFrame):
    dfBool = (oldFrame != newFrame).stack()
    diff = pd.concat([oldFrame.stack()[dfBool],
                      newFrame.stack()[dfBool]], axis=1)
    diff.columns = ["old", "new"]
    return diff
