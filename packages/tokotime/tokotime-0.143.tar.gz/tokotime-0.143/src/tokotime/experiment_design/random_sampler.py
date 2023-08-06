"""
Author:
   Alan Choon
"""

import pandas as pd
from tokotime.data_utils.utils import anti_join
from typing import List

class ExpGroupSplitter:
    def __init__(self, df: pd.DataFrame, idx_cols: List[str], 
                 cf_vars: List[str], treatment_split_props: List[float] = [0.3], 
                 seed: int = 2022) -> None:
        """
        This class is a wrapper that does an experimental split based on identifier columns
        provided and confounding variables to control for 
        
        Note that the confounding variable columns here must be categorical (must contain bin value belongs
        to if your original confounding variable is a continous variable)

        When the methods of the class are called sequentially, it will return a label for the exp_group
        (control / treatment_1 / treatment_2 .. etc)

        Refer to example_notebooks/exp_split.ipynb for example of usage

        Parameters:
            1. df: dataframe which contains the identifier columns & confounding var columns
            2. idx_cols: list of identifier columns to do the split on
            3. cf_vars: list of confounding variables to control for (must match column name in dataframe)
            4. treatment_split_props: list of proportion of entities to allocate to treatment group(s)
            5. seed: Random seed to set for splitting entities (Use the same seed for reproducibility)

        Attributes:
            1. df: dataframe which contains the identifier columns & confounding var columns
            2. idx_cols: list of identifier columns to do the split on
            3. cf_vars: list of confounding variables to control for (must match column name in dataframe)
            4. treatment_split_props: list of proportion of entities to allocate to treatment group(s)
            5. seed: Random seed to set for splitting entities (Use the same seed for reproducibility)
        """
        self.df = df
        self.idx_cols = idx_cols
        self.cf_vars = cf_vars
        self.treatment_split_props = treatment_split_props      # if more than one treatment group is required, pass in list of proportions
        self.seed = seed
        
    def stratified_sample_report(self) -> pd.DataFrame:
        """
        This method returns a dataframe which is a report, outlining the bin of confounding var the entity
        belongs to and the statistics of that bin

        Parameters:

        Returns:
            tmp_grpd: Dataframe containing experimental split report
        """
        population = len(self.df)
        tmp = self.df[self.cf_vars]
        tmp['size'] = 1
        tmp_grpd = tmp.groupby(self.cf_vars).count().reset_index()
        for k, treatment_split_prop in enumerate(self.treatment_split_props):
            tmp_grpd[f'treatment_{k+1}_samp_size'] = round(treatment_split_prop * tmp_grpd['size'])
        tmp_grpd = tmp_grpd[tmp_grpd['size'] > 0]
        return tmp_grpd
    
    def exclude_low_count_cf_vars(self, min_bin_size: float = None) -> None:
        """
        This method filters out entities belonging to confounding var value bins 
        with too low counts

        Parameters:

        Returns:
            None
        """
        sample_report = self.stratified_sample_report()
        if min_bin_size is None:
            min_bin_size = int(1/min(self.treatment_split_props))
        self.filtered_report = sample_report.loc[sample_report['size'] < min_bin_size]
        self.filtered_df = anti_join(self.df, self.filtered_report, self.cf_vars).drop_duplicates()
        self.df = self.filtered_df.merge(self.df, on=self.cf_vars, how='inner')
    
    def stratified_sampling(self) -> None:
        """
        This method does a randomized stratified split using the identifier columns
        to identify each entity to allocate for each split, stratification is done
        based on confounding variable bin value

        Parameters:
            
        Returns:
            None
        """
        population = len(self.df)
        tmp = self.df[self.cf_vars].copy()
        tmp.loc[:, 'size'] = 1
        tmp_grpd = tmp.groupby(self.cf_vars).count().reset_index()

        # controlling variable to create the dataframe or append to it
        stratified_samples = {f'treatment_{k+1}': [] for k in range(len(self.treatment_split_props))}
        for i in range(len(tmp_grpd)):
            # query generator for each iteration
            qry=''
            for cf_idx in range(len(self.cf_vars)):
                cf_var = self.cf_vars[cf_idx]
                confounding_var_value = tmp_grpd.iloc[i][cf_var]

                if type(confounding_var_value) == str:
                    confounding_var_value = "'" + str(confounding_var_value) + "'"

                if cf_idx != len(self.cf_vars)-1:
                    qry = qry + cf_var + ' == ' + str(confounding_var_value) + ' & '
                else:
                    qry = qry + cf_var + ' == ' + str(confounding_var_value)
            
            total_split_prop = sum(self.treatment_split_props)
            overall_sample_size = round(total_split_prop * tmp_grpd.iloc[i]['size'])
            stratified_sample = self.df.query(qry).sample(n=overall_sample_size, random_state=self.seed).reset_index(drop=True)
            idx = 0
            for k, treatment_split_prop in enumerate(self.treatment_split_props):
                treatment_sample_size = round(treatment_split_prop * tmp_grpd.iloc[i]['size'])
                stratified_sample_subset = stratified_sample.iloc[idx: idx + treatment_sample_size].copy()
                if stratified_sample_subset.shape[0] !=  0:
                    stratified_sample_subset.loc[:, 'exp_group'] = f'treatment_{k+1}'
                idx += treatment_sample_size
                stratified_samples[f'treatment_{k+1}'].append(stratified_sample_subset)
        
        self.treatment_dfs_dict = {k: pd.concat(df_lst) for k, df_lst in stratified_samples.items()}
    
    def get_control_treatment_split(self) -> None:
        """
        This method generates a column ('exp_group') that contains labels
        based on the experiment group each record belongs to
        (control, treatment_1, treatment_2, .. etc)

        Parameters:
            
        Returns:
            None
        """
        self.treatment_dfs_lst = [tdf for tdf in self.treatment_dfs_dict.values()]
        self.comb_treatment_df = pd.concat(self.treatment_dfs_lst)
        self.control_df = anti_join(self.df, self.comb_treatment_df, self.idx_cols)
        self.control_df = self.df.merge(self.control_df, on=self.idx_cols)
        self.control_df.loc[:, 'exp_group'] = 'control'
        self.results_df = pd.concat([self.comb_treatment_df, self.control_df])