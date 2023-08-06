import datetime
import pandas as pd
import math
import numpy as np
from typing import Callable, List
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

class BaseFeatureEngineer():
    def __init__(self, raw_df: pd.DataFrame, partition_cols: List[str],
                 date_col: str,
                 agg_funcs: List[Callable], metrics_cols: List[str], 
                 agg_periods: List[int] = [], 
                 shift_periods: List[int] = []):
        '''
        Initializes input parameters for feature engineering
        Parameters:
            raw_df: A pandas dataframe containing the raw metrics
            partition_cols: A list of column names that will be aggregated against
            agg_funcs: A list of aggregation functions to apply for feature engineering
            metrics_cols: The metrics metrics_columns we will be generating features on
            agg_periods: A list of integers representing historical window of time we want to 
                         aggregate against, if it's an empty list, then aggregate over all dates
        '''
        self.raw_df = raw_df
        self.partition_cols = partition_cols
        self.date_col = date_col
        self.agg_funcs = agg_funcs
        self.metrics_cols = metrics_cols
        self.agg_periods = agg_periods
        self.shift_periods = shift_periods
        self.window_feats = True if len(agg_periods) > 0 else False
        self.shift_feats = True if len(shift_periods) > 0 else False
        self.features_df = self.raw_df.copy()
        
    def sort_df(self):
        self.features_df.sort_values(by=self.partition_cols + [self.date_col], inplace=True)
        self.features_df = self.features_df.reset_index(drop=True)
            
    def engineer_window_feats(self):
        grouped_df = self.features_df.groupby(self.partition_cols)
        for metric_col in self.metrics_cols:
            for agg_func in self.agg_funcs:
                for agg_period in self.agg_periods:
                    renamed_col = f'fe_{agg_func.__name__}_{metric_col}_l{agg_period}d'
                    
                    self.features_df[renamed_col] = (grouped_df[metric_col].rolling(agg_period, closed='left')
                                                                .parallel_apply(agg_func, raw=True, engine='numba')
                                                    ).reset_index(drop=True)
                    

    def engineer_shift_feats(self):
        grouped_df = self.features_df.groupby(self.partition_cols)
        for metric_col in self.metrics_cols:
            for shift_t in self.shift_periods:
                renamed_col = f'fe_shift_{metric_col}_l{shift_t}d'
                self.features_df[renamed_col] = grouped_df[metric_col].shift(shift_t)
        
    def engineer_features(self):
        self.sort_df()
        if self.window_feats:
            self.engineer_window_feats()
        if self.shift_feats:
            self.engineer_shift_feats()
        
        if not self.window_feats and not self.shift_feats:
            for metric_col in self.metrics_cols:
                grouped_df = self.raw_df.groupby(self.partition_cols)
                self.features_df = (grouped_df[metric_col].agg(self.agg_funcs)
                            )
                self.features_df.columns = [x + "_" + metric_col for x in self.features_df.columns]
        return self.features_df

class DateFeatureEngineer():
    def __init__(self, df: pd.DataFrame, date_col: datetime.date, 
                 special_dates_feats_lst: List[str]):
        '''
        Initializes input parameters for date feature engineering
        Parameters:
            df: A pandas dataframe containing the raw metrics
            date_col: The column containing the date of records
            special_dates_feats_lst: A list of special date features to filter for
        '''
        self.df = df
        self.date_col = date_col
        self.special_dates_feats_lst = special_dates_feats_lst
        self.original_cols = list(df.columns)
    
    def engineer_features(self):
        self.df['fe_dayofmonth'] = pd.to_datetime(self.df[self.date_col]).dt.day.astype(np.int8)
        self.df['fe_dayofweek'] = pd.to_datetime(self.df[self.date_col]).dt.dayofweek.astype(np.int8)
        self.df['fe_weekofmonth'] = self.df['fe_dayofmonth'].apply(lambda x: math.ceil(x/7)).astype(np.int8)
        self.df['fe_is_weekend'] = (self.df['fe_dayofweek']>=5).astype(np.int8)
        self.df['fe_is_wib'] = (self.df['fe_dayofmonth'] >= 25).astype(int)
        self.df['fe_is_firstweek'] = (self.df['fe_dayofmonth'] <= 7).astype(int)
        self.df['fe_month'] = pd.to_datetime(self.df[self.date_col]).dt.month
        self.df['fe_is_double_date'] = (self.df['fe_dayofmonth'] == self.df['fe_month']).astype(int)
        return self.df[self.original_cols + self.special_dates_feats_lst]