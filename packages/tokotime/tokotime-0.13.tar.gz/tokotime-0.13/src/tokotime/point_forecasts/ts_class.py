"""
Author:
   Alan Choon, Anthony Jaya, Calvindoro Satyagraha
"""

import numpy as np
import pandas as pd
from typing import List

def label_demand_type(ts_series: pd.Series) -> str:
    '''
    Returns a string indication the time series classification of a series
    There are 5 possible labels, 'Unknown', 'Intermittent', 'Lumpy', 'Smooth', 'Erratic'
        Parameters:
            1. ts_series: A pandas series containing time series to be classified

        Returns:
            ts_label: Time series label
    '''
    if any(ts_series.isna()):
        return "Unknown"
    
    length = ts_series['length']
    summed = ts_series['summed']
    std = ts_series['std']
    mean = ts_series['mean']
    
    if summed == 0 or mean == 0:
        ts_label = "Unknown"
    else:
        adi = length/summed
        cv2 = std/mean
        if adi >= 1.32:
            if cv2 < 0.49:
                ts_label = "Intermittent"
            else:
                ts_label = "Lumpy"
        elif cv2 < 0.49:
            ts_label = "Lumpy"
    return ts_label

def get_demand_type_flag(df: pd.DataFrame, 
                         target_col: str, 
                         idx_cols: List[str], 
                         output_col: str) -> pd.DataFrame:
    '''
    Returns a dataframe containing time series classifications based on volatility and intermittency
    There are 5 possible labels, 'Unknown', 'Intermittent', 'Lumpy', 'Smooth', 'Erratic'
        Parameters:
            1. df: A grouped pandas dataframe to apply evaluation on
            2. target_col: Name of target col to do time series classification
            3. idx_cols: List of columns to aggregate against before ts classification
                                     (for eg: ['product_id', 'warehouse_id'])
            4. output_col: Name of output column containing flag generated

        Returns:
            df_result: Dataframe containing time series classification results
    '''
    df_agg = df.groupby([idx_cols]).agg(
        length = (target_col, lambda x : len(x)),
        summed = (target_col, lambda x : sum(x > 0)),
        std = (target_col, lambda x : (x[x>0].std(ddof = 0))),
        mean = (target_col, lambda x : x[x>0].mean())
    )
    df_agg[output_col] = df_agg.apply(label_demand_type, axis = 1)
    df_result = df_agg.reset_index()[idx_cols + [output_col]]
    return df_result