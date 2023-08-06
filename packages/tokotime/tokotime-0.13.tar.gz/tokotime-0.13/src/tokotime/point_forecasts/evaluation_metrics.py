"""
Author:
   Alan Choon, Anthony Jaya, Calvindoro Satyagraha
"""

import pandas as pd
import numpy as np
import functools as ft
from typing import Tuple, Callable, List


def calculate_mape(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a MAPE value (Mean Absolute Percentage Error)
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            mape: MAPE of predictions vs targets
    '''
    mask = targets > 0
    try:
        assert any(mask) # at least 1 value in mask is True
    except AssertionError:
        return np.nan # unidentified
    else:
        mape = np.fabs((targets[mask]-predictions[mask])/targets[mask]).mean()*100
        return mape

def calculate_mae(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a MAE value (Mean Absolute Error)
    This is a measure of model performance that is unscaled
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            mae: MAE of predictions vs targets
    '''
    residual = np.abs(targets-predictions)
    mae = np.mean(residual)
    return mae

def calculate_rmse(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a RMSE value (Root Mean Squared Error)
    This is a measure of model performance that is unscaled
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            rmse: RMSE of predictions vs targets
    '''
    rmse = np.sqrt(np.mean((targets-predictions)**2))
    return rmse

def calculate_maape(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a MAAPE value (Mean Arctangent Absolute Percetage Error)
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            maape: MAAPE of predictions vs targets
    '''
    # cause y_t = f_t = 0 will yield AAPE equals to undefined
    # then we dont consider if both actual and forecast contains zero
    yt0 = np.array(targets == 0)
    yp0 = np.array(predictions == 0)
    mask = ~(yt0 & yp0) # select all except both targets and predictions equals to 0
    try:
        assert any(mask) # at least 1 value in mask is True
    except AssertionError:
        return np.nan # unidentified
    else:
        actual = targets[mask]
        forecast = predictions[mask]
        actual[actual == 0] = 1e-12
        pctg_err = (actual - forecast) / actual
        APE = abs(pctg_err)
        AAPE = np.arctan(APE)
        return np.mean(AAPE)

def calculate_wape(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a WAPE value (Weighted Average Percentage Error)
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            wape: WAPE of predictions vs targets
    '''
    resids_summed = np.sum(abs(targets-predictions))
    targets_summed = np.sum(targets)
    if targets_summed == 0:
        return np.nan
    wape = resids_summed/targets_summed
    return wape

def calculate_wbpe(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a WBPE value (Weighted Bias Percentage Error)
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            wbpe: WBPE of predictions vs targets
    '''
    if np.sum(targets) == 0:
        return np.nan
    wbpe = np.sum(predictions-targets)/np.sum(targets)
    return wbpe

def calculate_pwape(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a pWAPE value (positive Weighted Average Percentage Error)
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            pwape: pWAPE of predictions vs targets
    '''
    resids_summed = np.sum(np.clip(predictions - targets, 0, None))
    targets_summed = np.sum(targets)
    if targets_summed == 0:
        return np.nan
    pwape = resids_summed/targets_summed
    return pwape

def calculate_nwape(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a nWAPE value (negative Weighted Average Percentage Error)
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            nwape: nWAPE of predictions vs targets
    '''
    resids_summed = np.sum(np.clip(targets - predictions, 0, None))
    targets_summed = np.sum(targets)
    if targets_summed == 0:
        return np.nan

    nwape = resids_summed/targets_summed
    return nwape

def calculate_wsdpe(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a WSDPE value (Weighted Standard Deviation Percentage Error)
    It measures how volatile the residuals are relative to the historical mean of the series
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            wsdpe: WSDPE of predictions vs targets
    '''
    denum = np.mean(targets)
    if denum == 0:
        return np.nan # unidentified
    else:
        wsdpe = np.sqrt(np.mean((targets-predictions)**2)) / denum
        return wsdpe

def evaluate_predictions(df: pd.DataFrame, prediction_cols: List[str], 
                         target_col: str, eval_func: Callable) -> pd.DataFrame:
    '''
    Returns a dataframe containing evaluation results of indicated prediction_cols vs target col
        Parameters:
            1. df: A grouped pandas dataframe to apply evaluation on
            2. prediction_cols: A list of column names containing predictions to evaluate
            3. target_col: Name of target col to evaluate against
            4. eval_func: Evaluation function to apply on predictions and target col

        Returns:
            results_df: Dataframe containing evaluation results
    '''
    out = []
    for col in prediction_cols:
        out.append(eval_func(df[target_col], df[col]))

    results_df = pd.Series(out)
    return results_df

def evaluate_by_segments(df: pd.DataFrame, prediction_cols: List[str], group_cols_lst: List[str], 
                         target_col: str, eval_func: Callable, print_results: bool = False) -> pd.DataFrame:
    '''
    Returns a dataframe containing evaluation results of indicated prediction_cols vs target col
        Parameters:
            1. df: A pandas dataframe to apply evaluation on
            2. prediction_cols: A list of column names containing predictions to evaluate
            3. group_cols_lst: A list of column names to act as index to aggregate evaluation results against
            4. target_col: Name of target col to evaluate against
            5. eval_func: Evaluation function to apply on predictions and target col

        Returns:
            eval_df: Dataframe containing evaluation results
    '''
    eval_dfs_lst = []
    
    for group_cols in group_cols_lst:
        eval_df = pd.DataFrame(df.groupby(group_cols).apply(lambda x : evaluate_predictions(x, prediction_cols, 
                                                                                            target_col, 
                                                                                            eval_func)))
        eval_df = eval_df.reset_index().groupby(group_cols).mean().T
        eval_df.index = prediction_cols
        eval_dfs_lst.append(eval_df)
        
    eval_df = pd.concat(eval_dfs_lst, axis = 1)
    
    if print_results:
        display(eval_df)
    return eval_df

def evaluate_by_segments_multiple_metrics(df: pd.DataFrame, prediction_cols: List[str], 
                                          group_cols_lst: List[str], 
                                          target_col: str,
                                          eval_funcs: Tuple[Callable, ...], 
                                          print_results: bool = False) -> pd.DataFrame:
    '''
    Returns a dataframe containing evaluation results of indicated prediction_cols vs target col
        Parameters:
            1. df: A pandas dataframe to apply evaluation on
            2. prediction_cols: A list of column names containing predictions to evaluate
            3. group_cols_lst: A list of column names to act as index to aggregate evaluation results against
            4. target_col: Name of target col to evaluate against
            5. eval_func: Evaluation function to apply on predictions and target col

        Returns:
            eval_df: Dataframe containing evaluation results
    '''
    eval_dfs_lst = []
    for eval_func in eval_funcs:
        eval_df = pd.DataFrame(df.groupby(group_cols_lst).apply(lambda x : evaluate_predictions(x, prediction_cols,
                                                                                                target_col,
                                                                                                eval_func))).reset_index()
        
        for i in range(len(prediction_cols)):
            eval_df.rename(columns={i: f"{eval_func.__name__}_{prediction_cols[i]}"}, inplace=True)
        eval_dfs_lst.append(eval_df)
    eval_final_df = ft.reduce(lambda left, right: pd.merge(left, right, on=group_cols_lst), eval_dfs_lst)
    eval_final_df.sort_values(by=group_cols_lst, inplace=True)
    if print_results:
        display(eval_df)
    return eval_final_df