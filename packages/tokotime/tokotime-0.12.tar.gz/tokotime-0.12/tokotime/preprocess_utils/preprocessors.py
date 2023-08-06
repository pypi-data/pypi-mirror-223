"""
Author:
   Alan Choon
"""

import pandas as pd
import numpy as np
from tokotime.preprocess_utils.preprocess_components import PreprocessFactory

class DefaultPreprocessor:
    '''
    This default preprocessor removes leading zero from each time series
    in the dataset, generated dates that are missing (ensure that all
    consecutive dates are filled in) and replaces missing values on
    given dates by 0
    '''
    def __init__(self, df: pd.DataFrame, preprocess_params: dict) -> None:
        self.df = df
        self.preprocess_params = preprocess_params

    def check_preprocess_params(self) -> None:
        req_preprocess_keys = ['id_columns',  'date_column', 'forecast_column']
        for k in req_preprocess_keys:
            if k not in self.preprocess_params:
                raise KeyError(f'{k} is a required key in preprocess_params!')

    
    def build_valid_params(self) -> None:
        
        if 'fill_missing_params' in self.preprocess_params:
            fill_missing_params = {'fill_missing': self.preprocess_params['fill_missing_params']}

        self.preprocess_params = {
            ## Dataframe is mutated by the transformers and dataframe is returned
            '': {
                'remove_leading_zero': {
                    'date_column': self.preprocess_params['date_column'],
                    'group_key': self.preprocess_params['id_columns'],
                    'forecast_column': self.preprocess_params['forecast_column']
                },
                'generate_missing_dates': {
                    'date_column': self.preprocess_params['date_column'],
                    'group_key': self.preprocess_params['id_columns']
                }
            },
        }

        self.preprocess_params[''] = {**self.preprocess_params[''], **fill_missing_params}
    
    def run(self) -> pd.DataFrame:
        self.check_preprocess_params()
        self.build_valid_params()
        preprocessed_df = PreprocessFactory(self.preprocess_params).execute(self.df)
        return preprocessed_df


class DefaultOOSImputer:
    '''
    This default OOS imputer impute observations from each time series
    based on the values of a given lookup column.
    The imputation methods used are 
    1) value of qty column + 1 &
    2) specified method by user
    The final imputed value is the max value of the outputs of the 2 methods above
    '''
    def __init__(self, df: pd.DataFrame, imputation_params: dict) -> None:
        self.df = df
        self.imputation_params = imputation_params
        self.impute_inplace = imputation_params.get('impute_inplace', False)
        self.ma_step_req_methods = ['mean', 'quantile_ex', 'min_max', 'quantile_in', 'median',
                                    'shift', 'ema_past', 'ema_recent']

    def check_imputation_params(self) -> None:
        req_preprocess_keys = ['id_columns',  'date_column', 
                               'forecast_column', 
                               'lookup_col',
                               'imputation_method',
                               'impute_params']
        for k in req_preprocess_keys:
            if k not in self.imputation_params:
                raise KeyError(f'{k} is a required key in preprocess_params!')

        if self.imputation_params['imputation_method'] in self.ma_step_req_methods:
            impute_params_options = self.imputation_params['impute_params']
            if 'ma' not in impute_params_options or 'step' not in impute_params_options:
                raise KeyError(f'ma and steps are required keys in impute_params for specified impute method')
        elif self.imputation_params['imputation_method'] not in ['bfill', 'ffill']:
            raise ValueError(f"{self.imputation_params['imputation_method']} imputation method is not implemented")

    def build_valid_params(self) -> None:
        self.col_params = {
            'lookup_col': self.imputation_params['lookup_col'],
            'forecast_column': self.imputation_params['forecast_column']
        }
        if self.imputation_params['imputation_method'] in self.ma_step_req_methods:
            fill_missing_options_params = {'update': self.imputation_params['date_column'],
                                           'ma': self.imputation_params['impute_params']['ma'], 
                                           'step': self.imputation_params['impute_params']['step']}
        else:
            fill_missing_options_params = {}
        self.imputation_params = {
            '': {
                'add_mapped_column': {
                    'params':[
                        {
                            'src_column': self.imputation_params['date_column'],
                            'dst_column': 'day_of_week',
                            'fn': lambda x: x.weekday(),
                        },
                        {
                            'src_column': self.imputation_params['forecast_column'],
                            'dst_column': 'qty1',
                            'fn': lambda q: q + 1,
                        }
                    ],
                    'size': 2,
                },
                'fill_missing': {
                    'params': [
                        {
                            'column': 'imputed',
                            'method': self.imputation_params['imputation_method'],
                            'options': fill_missing_options_params,
                            'groupby': self.imputation_params['id_columns'], 
                        },
                    ],
                    'size': 1
                },
                'post_round': {'force': True},
            },
        }

    def impute(self) -> pd.DataFrame:
        self.check_imputation_params()
        self.build_valid_params()
        ## Check that the lookup column has values 0, 1 
        # (impute all records with value lookup == 1)
        lookup_col = self.col_params['lookup_col']
        if self.df[self.df[lookup_col] == 1].shape == 0:
            raise ValueError("Lookup column for data imputation must have values 0, 1")
        X = self.df.copy()
        X.loc[:, 'imputed'] = X[self.col_params['forecast_column']].copy()
        X.loc[X[lookup_col] == 1, f'imputed_{self.col_params["forecast_column"]}'] = np.nan
        X = PreprocessFactory(self.imputation_params).fit_transform(X)
        final_impute_column = self.col_params["forecast_column"] if self.impute_inplace else f'imputed_{self.col_params["forecast_column"]}'
        X.loc[X[lookup_col] == 1, final_impute_column] = X.loc[X[lookup_col] == 1, ['imputed', 'qty1']].progress_apply(max, axis=1)
        cols_to_be_dropped = ['qty1', 'day_of_week', 'imputed'] 
        if self.impute_inplace:
            cols_to_be_dropped.append(f'imputed_{self.col_params["forecast_column"]}')
        X.drop(columns=cols_to_be_dropped, inplace=True)
        return X