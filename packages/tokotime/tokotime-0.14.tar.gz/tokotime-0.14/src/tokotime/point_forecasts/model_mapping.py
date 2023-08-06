
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor, LGBMClassifier
from sklego.meta import ZeroInflatedRegressor
from sktime.forecasting.croston import Croston
from sktime.forecasting.naive import NaiveForecaster
from pmdarima.arima import AutoARIMA
from tokotime.point_forecasts.model_wrappers import SciKitLocalModel, STLLocalModel, ZIRLocalModel, SKTimeLocalModel, PMDAutoArimaLocalModel, MovingAverageLocalModel

def map_model_regressor(model_name: str, **kwargs):
    classifier_params = kwargs.get('classifier_params', {})
    regressor_params = kwargs.get('regressor_params', {})
    assert isinstance(classifier_params, dict), "classifier_params must be in the form of a dictionary"
    assert isinstance(regressor_params, dict), "regressor_params must be in the form of a dictionary"
    regressor_mapping = {
            'local_lgb': LGBMRegressor(n_jobs = 1, verbose = -1, **regressor_params),
            'local_lgb_stl': LGBMRegressor(n_jobs = 1, verbose = -1, **regressor_params),
            'local_lgb_stl_resid': LGBMRegressor(n_jobs = 1, verbose = -1, **regressor_params),
            'global_lgb': LGBMRegressor(n_jobs = 1, verbose = -1, **regressor_params),
            'local_lgb_zir': ZeroInflatedRegressor(
                                    classifier=LGBMClassifier(n_jobs = 1, verbose = -1, **classifier_params),
                                    regressor=LGBMRegressor(n_jobs = 1, verbose = -1, **regressor_params)
                             ),
            'local_crouston': Croston(smoothing=kwargs['smoothing']) if 'smoothing' in kwargs else Croston(smoothing=0.1),
            'naive_mean': NaiveForecaster(strategy='mean'),
            'naive_last': NaiveForecaster(strategy='last'),
            'local_auto_arima': AutoARIMA(**regressor_params),
            'local_moving_average': None
        }
    assert model_name in regressor_mapping, f"model: {model_name} is not implemented yet!"
    return regressor_mapping[model_name]

def map_model_wrapper_class(model_name: str):
    if model_name in ['local_lgb']:
        return SciKitLocalModel()
    elif 'stl' in model_name:
        return STLLocalModel()
    elif model_name == 'local_lgb_zir':
        return ZIRLocalModel()
    elif model_name in ['local_crouston', 'naive_mean', 'naive_last']:
        return SKTimeLocalModel()
    elif model_name in ['local_auto_arima']:
        return PMDAutoArimaLocalModel()
    elif model_name in ['local_moving_average']:
        return MovingAverageLocalModel()
    else:
        raise ValueError(f"Model {model_name} is not implemented yet")

