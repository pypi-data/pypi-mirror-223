import pandas as pd
import numpy as np
import lightgbm as lgb
import optuna
import warnings
warnings.filterwarnings("ignore")
from optuna.integration import LightGBMPruningCallback
optuna.logging.set_verbosity(optuna.logging.ERROR)
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
from tqdm import tqdm

class BayesianHPTuner():
    def __init__(self, train_df, features, target, objective_metric='tweedie',
                eval_metric='rmse'):
        self.train_df = train_df
        self.features = features
        self.target = target
        self.objective_metric = objective_metric
        self.eval_metric = eval_metric
    
    def objective(self, trial, X, y):
        param_grid = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 1500, step=100),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "num_leaves": trial.suggest_int("num_leaves", 20, 2000, step=20),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "min_child_samples": trial.suggest_int("min_data_in_leaf", 200, 10000, step=100),
            "min_split_gain": trial.suggest_float("min_gain_to_split", 0, 15),
            "subsample": trial.suggest_float(
                "subsample", 0.2, 0.9, step=0.1
            ),
            "colsample_bytree": trial.suggest_float(
                "colsample_bytree", 0.2, 0.9, step=0.1
            ),
            "verbose": trial.suggest_categorical("verbose", [-1])
        }
        
        if self.objective_metric == 'tweedie':
            param_grid["tweedie_variance_power"] = trial.suggest_float("tweedie_variance_power", 1, 1.9, step=0.1)
        
        tscv = TimeSeriesSplit(n_splits=5)

        tscv_scores = np.empty(5)
        for idx, (train_idx, test_idx) in enumerate(tscv.split(X)):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            model = lgb.LGBMRegressor(objective=self.objective_metric, boosting_type="gbdt",
                                      **param_grid)
            model.fit(
                X_train,
                y_train,
                eval_set=[(X_test, y_test)],
                eval_metric=self.eval_metric,
                early_stopping_rounds=100,
                callbacks=[
                    LightGBMPruningCallback(trial, self.eval_metric)
                ],
            )
            preds = model.predict(X_test)
            tscv_scores[idx] = np.sqrt(mean_squared_error(y_test, preds))

        return np.mean(tscv_scores)
    
    def tune_best_hp(self):
        self.train_df = self.train_df.reset_index(drop=True)
        study = optuna.create_study(direction="minimize", study_name="LGBM Classifier")
        func = lambda trial: self.objective(trial, self.train_df[self.features], self.train_df[self.target])
        study.optimize(func, n_trials=100)
        best_params = study.best_params
        best_params.pop("verbose")
        return best_params