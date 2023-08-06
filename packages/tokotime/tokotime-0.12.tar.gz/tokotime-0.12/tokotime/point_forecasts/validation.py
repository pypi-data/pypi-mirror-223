import datetime
import pandas as pd
import numpy as np
from typing import Tuple, List

def train_test_ts_split(df: pd.DataFrame, 
                     id_cols: List[str],
                     date_col: str,
                     test_start_date: datetime.date, 
                     test_end_date: datetime.date,
                     min_len: int = 30) -> Tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Returns 2 dataframes, 1 containing observations in train set and the other contains
    observations in test set.
        Parameters:
            1. df: Dataframe to be split by train and test
            2. id_cols: identifier columns in dataframe 
            3. date_col: date column in dataframe to be split by
            4. test_start_date
            5. test_end_date
            6. min_len: minimum length of each time series to be included in train-test split

        Returns:
            train_data: Training data for model to be fitted on
            test_data: Test/Validation data
    '''
    train_end_date = test_start_date - datetime.timedelta(days=1)
    min_start_date = train_end_date - datetime.timedelta(days=min_len)
    # Create a temp col that combines all identifiers:
    df['temp_id'] = df[id_cols].astype(str).apply(lambda x: '_'.join(x.dropna().values.tolist()), axis=1)
    min_max_date = df.groupby('temp_id').agg({date_col: ['min', 'max']}).reset_index()
    valid_obs = min_max_date[min_max_date[(date_col, 'min')] <= min_start_date].temp_id.unique()
    filtered_df = df[df['temp_id'].isin(valid_obs)].reset_index(drop = True)
    test_data = filtered_df[(filtered_df[date_col] <= test_end_date) & 
                              (filtered_df[date_col] >= test_start_date)].reset_index(drop = True)
    train_data = filtered_df[filtered_df[date_col] <= train_end_date].reset_index(drop = True)
    train_data = train_data.sort_values(['temp_id', date_col]).reset_index(drop = True)
    test_data = test_data.sort_values(['temp_id', date_col]).reset_index(drop = True)
    train_data.drop(columns=['temp_id'], inplace=True)
    test_data.drop(columns=['temp_id'], inplace=True)
    return train_data, test_data