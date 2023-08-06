"""
Author:
   Alan Choon
"""
import datetime
import numpy as np
import pandas as pd
import multiprocessing as mp
import mpire
from mpire import WorkerPool
from tokotime.point_forecasts.model_mapping import map_model_regressor, map_model_wrapper_class
from tokotime.point_forecasts.misc import day_date_map
from tokotime.hp_tune.bayes_hp_tuner import BayesianHPTuner

class LocalModelRunner():
    def __init__(self, train_data: pd.DataFrame, model_params: dict,
                exog_df: pd.DataFrame = None) -> None:
        self.train_data = train_data
        self.dataset_metadata = model_params["dataset_metadata"]
        self.forecast_params = model_params["forecast_params"]
        self.exog_df = exog_df
        
    def fit_predict(self) -> None:
        '''
       This method fits a training set on a regressor and predicts forecast_periods days into the future
        '''
        def forecast_individual(iterator: int, 
                                train: pd.DataFrame = self.train_data,
                                forecast_params: dict = self.forecast_params,
                                dataset_metadata: dict = self.dataset_metadata) -> pd.DataFrame:
            id_col = self.dataset_metadata['id']
            date_col = self.dataset_metadata['date']
            target_col = self.dataset_metadata['target']
            model_name = self.forecast_params['model_name']
            forecast_period = self.forecast_params['forecast_horizon']
            output_col = self.forecast_params['output_col_name']
            model_params = self.forecast_params.get('model_params', {})
            max_date = train[date_col].max()
            ### Select individual time series
            selected_train = train[train[id_col] == iterator].reset_index(drop = True)
            
            model_wrapper = map_model_wrapper_class(model_name)
            self.forecast_params['regressor'] = map_model_regressor(model_name, **model_params)
            if model_name == 'local_auto_arima' and 'exog_feats' in forecast_params:
                selected_train = selected_train[[id_col, date_col, target_col] + forecast_params['exog_feats']]
                df_fcast = model_wrapper.fit_predict_rolling(selected_train, self.forecast_params, 
                                                             self.dataset_metadata, exog_df=self.exog_df)
            else:
                selected_train = selected_train[[id_col, date_col, target_col]]
                df_fcast = model_wrapper.fit_predict_rolling(selected_train, self.forecast_params, 
                                                             self.dataset_metadata)
            df_fcast = day_date_map(df_fcast, forecast_period,
                                    max_date,
                                    output_date_col=date_col)
            df_fcast[id_col] = iterator
            return df_fcast[[id_col, date_col, 'model_name', output_col]]
        
        list_of_id = self.forecast_params['forecast_id']

        num_cores = mp.cpu_count()
        
        ### Parallelization using mpire library
        with WorkerPool(n_jobs=num_cores) as pool:
            result_list = pool.map_unordered(forecast_individual, list_of_id, progress_bar = True)
        
        ### Sorting the output
        df_result = pd.concat(result_list).sort_values([self.dataset_metadata['id'], 
                                                        self.dataset_metadata['date']]).reset_index(drop = True)
        return df_result

class GlobalModelRunner():
    def __init__(self, dataset: pd.DataFrame, model_params: dict) -> None:
        self.dataset = dataset
        self.dataset_metadata = model_params["dataset_metadata"]
        self.forecast_params = model_params["forecast_params"]

class GlobalModelSlidingRunner(GlobalModelRunner):
    def gen_inference_data(self) -> None:
        item_col = self.dataset_metadata['id']
        date_col = self.dataset_metadata['date']
        unique_items = self.dataset[item_col].unique()
        forecast_horizon = self.forecast_params['forecast_horizon']
        categories_col = [forecast_params['model_category']] if 'model_category' in self.forecast_params else []
        sel_cols = [item_col] + categories_col
        inference_items_df = self.dataset[sel_cols].drop_duplicates()
        self.forecast_start_date = pd.to_datetime(self.dataset[date_col]).dt.date.max()
        self.forecast_end_date = self.forecast_start_date + datetime.timedelta(days=forecast_horizon-1)
        date_df = pd.date_range(self.forecast_start_date, self.forecast_end_date).to_frame(name=date_col).reset_index(drop=True)
        item_dates_combi_df = inference_items_df.merge(date_df, how='cross')
        item_dates_combi_df[date_col] = item_dates_combi_df[date_col].dt.date
        self.dataset = pd.concat([self.dataset, item_dates_combi_df])

    def shift_feats(self) -> None:
        shift_window = self.forecast_params['forecast_horizon']
        for feat in self.forecast_params['agg_feats']:
            self.dataset[feat] = self.dataset.groupby(self.dataset_metadata['id'])[feat].shift(shift_window)

    def train_inference_split(self) -> None:
        date_col = self.dataset_metadata['date']
        self.gen_inference_data()
        self.shift_feats()
        self.inference_data = self.dataset[(pd.to_datetime(self.dataset[date_col]).dt.date >= self.forecast_start_date) & \
                                           (pd.to_datetime(self.dataset[date_col]).dt.date <= self.forecast_end_date)]
        self.train_data = self.dataset[(pd.to_datetime(self.dataset[date_col]).dt.date < self.forecast_start_date)]
        del self.dataset
        
    def tune_hp(self, model_params: dict) -> dict:
        if 'regressor_params' in model_params:
            regressor_params = model_params.get('regressor_params', 'regression')
        else:
            regressor_params = {'objective': 'regression'}
        if model_params['hp_tune'] == 'bayes':
            bayes_tuner = BayesianHPTuner(self.train_data, self.feats, self.target_col,
                                          objective_metric=regressor_params['objective'],
                                          eval_metric=regressor_params.get('eval_metric', 'rmse'))
            best_hp = bayes_tuner.tune_best_hp()
            best_hp['objective'] = regressor_params['objective']
            return best_hp
        else:
            raise ValueError(f"HP tune method: {model_params['hp_tune']} has not been implemented")

    def fit(self) -> None:
        self.train_inference_split()
        self.category_models_map = {}
        self.feats = self.forecast_params['feats']
        self.target_col = self.dataset_metadata['target']
        self.model_name = self.forecast_params['model_name']
        model_params = self.forecast_params.get('model_params', {})
        if 'hp_tune' in model_params:
            model_params['regressor_params'] = self.tune_hp(model_params)
        
        # Enable this in the case where we want to train a model per category
        if 'model_category' in self.forecast_params:
            self.category_models_enabled = True
            categories_col = forecast_params['model_category']
            self.model_categories = self.train_data[categories_col].unique()
            for cat in self.model_categories:
                self.forecast_params['regressor'] = map_model_regressor(self.model_name, **model_params)
                train_sub_df = self.train_data[self.train_data[categories_col] == cat]
                cat_regressor = self.forecast_params['regressor'].fit(train_sub_df[self.feats],
                                                                      train_sub_df[self.target_col])
                self.category_models_map[cat] = cat_regressor
        else:
            self.category_models_enabled = False
            self.forecast_params['regressor'] = map_model_regressor(self.model_name, **model_params)
            self.forecast_params['regressor'].fit(self.train_data[self.feats],
                                                  self.train_data[self.target_col])
            self.category_models_map['ALL'] = self.forecast_params['regressor']

    def predict(self) -> None:
        output_col_name = self.forecast_params['output_col_name']
        item_col = self.dataset_metadata['id']
        date_col = self.dataset_metadata['date']
        preds_df_lst = []
        if self.category_models_enabled:
            categories_col = forecast_params['model_category']
            for cat in self.category_models_map:
                infer_sub_df = self.inference_data[self.inference_data[categories_col] == cat]
                cat_regressor = self.category_models_map[cat]
                infer_sub_df[output_col_name] = self.forecast_params['regressor'].predict(infer_sub_df[self.feats])
                infer_sub_df['model_name'] = self.model_name
                infer_sub_df = infer_sub_df[[item_col, date_col, 'model_name', output_col_name]]
                preds_df_lst.append(infer_sub_df)
        else:
            self.inference_data[output_col_name] = self.forecast_params['regressor'].predict(self.inference_data[self.feats])
            self.inference_data['model_name'] = self.model_name
            preds_df_lst.append(self.inference_data[[item_col, date_col, 
                                                     'model_name', output_col_name]])
        predictions_df = pd.concat(preds_df_lst)
        return predictions_df

    def fit_predict(self) -> None:
        '''
        This method fits a training set on a regressor and predicts forecast_periods days into the future
        '''
        self.fit()
        return self.predict()