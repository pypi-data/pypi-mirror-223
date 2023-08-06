"""
Author:
   Alan Choon
"""
import logging
import numpy as np
import pandas as pd
import datetime
from statsmodels.tsa.seasonal import STL
from darts import TimeSeries
from darts.models import (
    RegressionModel
)
from pmdarima.arima import AutoARIMA
from threadpoolctl import threadpool_limits

class LocalModel():
    '''
    This class is a parent class for all Local Model wrappers
    '''
    def _init_vars(self, train: pd.DataFrame, 
                   forecast_params: dict, dataset_metadata: dict) -> None:
        self.forecast_periods = forecast_params['forecast_horizon']
        self.seasonal_period = forecast_params.get('seasonal_period', 7)
        self.model_name = forecast_params['model_name']
        self.regressor = forecast_params['regressor']
        self.output_col_name = forecast_params['output_col_name']
        self.train = train
        self.target_col = dataset_metadata['target']
        self.id_col = dataset_metadata['id']
        self.date_col = dataset_metadata['date']
        
class MovingAverageLocalModel(LocalModel):
    '''
    This class is a wrapper for regressor models with sklearn-like methods for 
    time-series regression
    '''
        
    def fit_rolling(self, train: pd.DataFrame, forecast_params: dict, dataset_metadata: dict) -> None:
        self._init_vars(train, forecast_params, dataset_metadata)
        self.ma = forecast_params['model_params']['ma']             # Only for Moving Average models
        
    def predict_rolling(self) -> None:
        rolling_predict = self.train[self.target_col][-self.ma:].values
        for i, fp in enumerate(range(self.forecast_periods)):
            prediction_array = rolling_predict[-self.ma:]
            single_predict = np.mean(prediction_array)
            rolling_predict = np.append(rolling_predict, single_predict)
            
        forecast_col = self.output_col_name
        df_fcast = pd.DataFrame()
        df_fcast[forecast_col] = rolling_predict[-self.forecast_periods:]
        df_fcast['day'] = list(range(self.forecast_periods))
        df_fcast['model_name'] = self.model_name
        return df_fcast
    
    def fit_predict_rolling(self, train: pd.DataFrame, 
                            forecast_params: dict, dataset_metadata: dict) -> None:
        self.fit_rolling(train, forecast_params, dataset_metadata)
        return self.predict_rolling()

class SciKitLocalModel(LocalModel):
    '''
    This class is a wrapper for regressor models with sklearn-like methods for 
    time-series regression
    ''' 
    def feature_engineer(self) -> None:
        self.lag_length = int(self.train.shape[0]*0.6)
        ### Creating training matrix
        train_matrix = pd.DataFrame()
        lagged_feats_series = []
        for lag in range(self.lag_length, -1, -1):
            lagged_feats_series.append(self.train.groupby(self.id_col)[self.target_col].shift(lag).rename(f't-{lag}'))
        train_matrix = pd.concat(lagged_feats_series, axis=1)
            # train_matrix[f't-{lag}'] = self.train.groupby(self.id_col)[self.target_col].shift(lag)
        self.train_matrix = train_matrix.dropna().reset_index(drop = True)
        
    def fit_rolling(self, train: pd.DataFrame, forecast_params: dict, dataset_metadata: dict) -> None:
        self._init_vars(train, forecast_params, dataset_metadata)
        self.feature_engineer()
        x = self.train_matrix.iloc[:,:-1]
        y = self.train_matrix.iloc[:,-1:]
        self.regressor.fit(x, y.values.ravel())
        
    def predict_rolling(self) -> None:
        to_predict = self.train_matrix.tail(1).copy()
        rolling_predict = to_predict.values[0]
        for fp in range(self.forecast_periods):
            prediction_array = rolling_predict[-self.lag_length:].reshape(-1, self.lag_length)
            single_predict = self.regressor.predict(prediction_array)
            rolling_predict = np.append(rolling_predict, single_predict)
            
        forecast_col = self.output_col_name
        df_fcast = pd.DataFrame()
        df_fcast[forecast_col] = rolling_predict[-self.forecast_periods:]
        df_fcast['day'] = list(range(self.forecast_periods))
        df_fcast['model_name'] = self.model_name
        return df_fcast
    
    def fit_predict_rolling(self, train: pd.DataFrame, 
                            forecast_params: dict, dataset_metadata: dict) -> None:
        self.fit_rolling(train, forecast_params, dataset_metadata)
        return self.predict_rolling()


class STLLocalModel(LocalModel):
    '''
    This class is a wrapper for regressor models with sklearn-like methods for 
    time-series regression
    '''

    @staticmethod
    def repeat_seasonal(seasonal_df: pd.DataFrame, day: int) -> pd.DataFrame:
        seasonal_df = pd.DataFrame(seasonal_df)
        result = pd.concat([seasonal_df, seasonal_df.iloc[-day:]])
        result.reset_index(inplace=True, drop=True)
        return result.iloc[-day:]

    def univar_lgbm(self, df: pd.DataFrame, forecast_period=28) -> np.array:
        ts = TimeSeries.from_dataframe(df.reset_index(), time_col='ds')
        model = RegressionModel(lags=self.lag_length, 
                                model=self.regressor)
        model.fit(ts)
        univar_lgbm_fcast = model.predict(forecast_period)
        return univar_lgbm_fcast.pd_series().values

    def fit_predict_rolling(self, train: pd.DataFrame, 
                            forecast_params: dict, dataset_metadata: dict) -> pd.DataFrame:
        self._init_vars(train, forecast_params, dataset_metadata)
        self.lag_length = int(self.train.shape[0]*0.6)
        ts = train[[self.date_col, self.target_col]]
        ts = ts.rename(columns={self.date_col: 'ds',
                                self.target_col: 'y'})
        ts['ds'] = pd.to_datetime(ts['ds'])
        ts = ts.set_index('ds')
        df_output = pd.DataFrame()

        # forecast for mstl and mstl_resid LGB
        stl = STL(ts["y"], period=self.seasonal_period)
        res = stl.fit()

        # STL decomposition
        seasonal_df = pd.DataFrame(res.seasonal)
        trend_df = res.trend
        res_df = res.resid

        forecast_col = self.output_col_name
        result = self.repeat_seasonal(seasonal_df, self.forecast_periods)
        result['trend'] = self.univar_lgbm(trend_df, forecast_period=self.forecast_periods)
        result[f'{self.model_name}_fc'] = (result.sum(axis = 1)).astype(int)
        result['resid'] = self.univar_lgbm(res_df, forecast_period=self.forecast_periods)
        result[forecast_col] = (result['season'] + result['trend'] + result['resid']).astype(int)
        df_output = result[[forecast_col]].copy()
        df_output.set_index(result.index)
        df_output['day'] = list(range(self.forecast_periods))
        df_output['model_name'] = self.model_name
        return df_output


class ZIRLocalModel(SciKitLocalModel):
    def fit_rolling(self, train: pd.DataFrame, forecast_params: dict, dataset_metadata: dict) -> pd.DataFrame:
        self._init_vars(train, forecast_params, dataset_metadata)
        self.feature_engineer()
        x = self.train_matrix.iloc[:,:-1]
        y = self.train_matrix.iloc[:,-1:]

        # Workaround in case classifier returns all zero values
        x = x + 1
        y = y + 1

        self.regressor.fit(x, y.values.ravel())

    def predict_rolling(self) -> pd.DataFrame:
        to_predict = self.train_matrix.tail(1).copy()
        rolling_predict = to_predict.values[0]
        for fp in range(self.forecast_periods):
            prediction_array = rolling_predict[-self.lag_length:].reshape(-1, self.lag_length)
            single_predict = self.regressor.predict(prediction_array)

            ### If the prediction result is more than 2.5 times the maximum of the time series, set it to the max value
            ### (in a way this is the forecast protector)
            if single_predict > np.max(rolling_predict) * 2.5:
                single_predict = np.max(rolling_predict)
            elif np.isnan(single_predict):
                single_predict = 0
            elif single_predict < 0:
                single_predict = 0

            rolling_predict = np.append(rolling_predict, single_predict)
            
        df_fcast = pd.DataFrame()
        forecast_col = self.output_col_name
        df_fcast[forecast_col] = rolling_predict[-self.forecast_periods:]
        df_fcast[forecast_col] = np.round(df_fcast[forecast_col], 0)
        df_fcast[forecast_col] = df_fcast[forecast_col].astype(int)  - 1
        df_fcast['day'] = list(range(self.forecast_periods))
        df_fcast['model_name'] = self.model_name
        return df_fcast


class SKTimeLocalModel(LocalModel):
    def fit_rolling(self, train: pd.DataFrame, 
                    forecast_params: dict, 
                    dataset_metadata: dict) -> None:
        self._init_vars(train, forecast_params, dataset_metadata)
        y = self.train[self.target_col]
        self.regressor.fit(y.values.ravel())

    def predict_rolling(self) -> pd.DataFrame:
        fh = np.arange(1, self.forecast_periods + 1)
        rolling_predict = self.regressor.predict(fh=fh)        
        df_fcast = pd.DataFrame()
        forecast_col = self.output_col_name
        df_fcast[forecast_col] = rolling_predict[-self.forecast_periods:, 0]
        df_fcast['day'] = list(range(self.forecast_periods))
        df_fcast['model_name'] = self.model_name
        return df_fcast

    def fit_predict_rolling(self, train: pd.DataFrame, 
                            forecast_params: dict, dataset_metadata: dict) -> pd.DataFrame:
        self.fit_rolling(train, forecast_params, dataset_metadata)
        return self.predict_rolling()

class PMDAutoArimaLocalModel(LocalModel):
    '''
    This class is a wrapper for AutoARIMA from pmdarima.arima library
    '''
    def generate_future_dataframe(self, train):
        fh = np.arange(1, self.forecast_periods + 1)       
        df_fcast = pd.DataFrame()
        max_date = train[self.date_col].max()
        df_fcast['day'] = list(range(self.forecast_periods))
        day_date_map = {i: max_date + datetime.timedelta(days=i+1) for i in range(self.forecast_periods)}
        df_fcast[self.date_col] = df_fcast['day'].map(day_date_map)
        return df_fcast
    
    def fit_predict_rolling(self, train: pd.DataFrame, 
                    forecast_params: dict, 
                    dataset_metadata: dict,
                    exog_df: pd.DataFrame = None) -> None:
        self._init_vars(train, forecast_params, dataset_metadata)
        y = self.train[self.target_col]
        model = AutoARIMA(n_jobs = 1)
        if 'exog_feats' in forecast_params:
            assert exog_df is not None, "Exogenous dataframe must be passed when exog_feats are set in forecast_params!"
            merged_df = self.train.merge(exog_df, on=[self.id_col, self.date_col], how='inner')
            assert self.train.shape[0] == len(y), "Records in Exogenous DF does not fit training df!"
            hist_feats = self.train[forecast_params['exog_feats']]
            future_df = self.generate_future_dataframe(self.train)
            try :
                with threadpool_limits(limits=1, user_api='blas'): # Limit number of threading because autoarima will use all threads even if n_jobs = 1, which lead to bottle neck when applying multiprocessing
                    model.fit(y=y, X=hist_feats.values)
                    forecast_col = self.output_col_name
                    future_df = future_df.merge(exog_df, on=[self.id_col, self.date_col], how='inner')
                    assert future_df.shape[0] == int(self.forecast_periods), "Records in Exogenous DF does not fit required forecast horizon!"
                    fcasts = model.predict(int(self.forecast_periods), X=future_X)
                    future_df[forecast_col] = np.clip(fcasts.values, a_min=0, a_max=None)
                    future_df['model_name'] = self.model_name
                    return future_df
            except Exception as e : # Sometime autoarima failed to find the best model, if that happen then we change the prediction into 7 day average prediction
                logging.info(e)
                fcasts = pd.Series([self.train[self.target_col].tail(7).mean()]*self.forecast_periods)
                future_df = self.generate_future_dataframe(self.train)
                future_df[forecast_col] = fcasts
                future_df['model_name'] = 'ma_7'
                return future_df
        else:
            future_df = self.generate_future_dataframe(self.train)
            try :
                with threadpool_limits(limits=1, user_api='blas'): # Limit number of threading because autoarima will use all threads even if n_jobs = 1, which lead to bottle neck when applying multiprocessing
                    model.fit(y=y)
                    forecast_col = self.output_col_name
                    fcasts = model.predict(int(self.forecast_periods))
                    future_df[forecast_col] = np.clip(fcasts.values, a_min=0, a_max=None)
                    future_df['model_name'] = self.model_name
                    return future_df
            except Exception as e : # Sometime autoarima failed to find the best model, if that happen then we change the prediction into 7 day average prediction
                logging.info(e)
                fcasts = pd.Series([self.train[self.target_col].tail(7).mean()]*self.forecast_periods)
                future_df = self.generate_future_dataframe(self.train)
                future_df[forecast_col] = fcasts
                future_df['model_name'] = 'ma_7'
                return future_df