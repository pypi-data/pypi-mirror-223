import functools as ft
import numpy as np
import pandas as pd
from typing import Tuple, Callable, List


class Evaluator:
    def __init__(df: pd.DataFrame, prediction_cols: List[str], 
                 group_cols_lst: List[str], 
                 target_col: str,
                 eval_funcs: Tuple[Callable, ...]):
        '''
        Parameters:
                1. df: A pandas dataframe to apply evaluation on
                2. prediction_cols: A list of column names containing predictions to evaluate
                3. group_cols_lst: A list of column names to act as index to aggregate evaluation results against
                4. target_col: Name of target col to evaluate against
                5. eval_func: Evaluation function to apply on predictions and target col

        '''
        self.df = df
        self.prediction_cols = prediction_cols
        self.group_cols_lst = group_cols_lst
        self.target_col = target_col
        self.eval_funcs = eval_funcs


    def evaluate(self) -> pd.DataFrame:
        '''
        Returns a dataframe containing evaluation results of indicated prediction_cols vs target col
            Returns:
                eval_df: Dataframe containing evaluation results
        '''
        eval_dfs_lst = []
        for eval_func in self.eval_funcs:
            eval_df = pd.DataFrame(self.df.groupby(self.group_cols_lst)
                                          .apply(lambda x : evaluate_predictions(x, self.prediction_cols,
                                                                                 self.target_col, 
                                                                                 eval_func))).reset_index()
            eval_df['eval_function'] = eval_func.__name__
            
            eval_dfs_lst.append(eval_df)
        eval_final_df = pd.concat(eval_dfs_lst)
        eval_final_df.sort_values(by=self.group_cols_lst, inplace=True)
        eval_final_df = eval_final_df[['segment', 'prediction_type', 'eval_function', 'eval_value']]
        return eval_final_df