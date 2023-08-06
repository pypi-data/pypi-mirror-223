"""
Author:
   Alan Choon, Anthony Jaya, Calvindoro Satyagraha
"""

import pandas as pd
import numpy as np
import functools as ft


def calculate_sla(targets: np.array, predictions: np.array) -> float:
    '''
    Returns a SLA value (Service Level Agreement)
    This metric measures the percentage of times the forecasts are higher or equal to actual values
        Parameters:
            1. targets: A numpy array containing target values
            2. predictions: A numpy array containing forecasts

        Returns:
            sla: SLA of predictions vs targets
    '''
    if len(targets):
        sla = float((predictions >= targets).sum()) / len(targets)
        return sla
    else:
        return np.nan
