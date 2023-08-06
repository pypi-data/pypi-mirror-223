"""
Author:
   Alan Choon, Anthony Jaya, Calvindoro Satyagraha
"""

import pandas as pd
import numpy as np
import functools as ft
from typing import Tuple, Callable, List


def MAPE(targets: np.array, predictions: np.array) -> float:
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

def MAE(targets: np.array, predictions: np.array) -> float:
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

def RMSE(targets: np.array, predictions: np.array) -> float:
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

def MAAPE(targets: np.array, predictions: np.array) -> float:
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

def WAPE(targets: np.array, predictions: np.array) -> float:
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

def WBPE(targets: np.array, predictions: np.array) -> float:
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

def PWAPE(targets: np.array, predictions: np.array) -> float:
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

def NWAPE(targets: np.array, predictions: np.array) -> float:
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

def WSDPE(targets: np.array, predictions: np.array) -> float:
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