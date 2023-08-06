"""
Author:
   Alan Choon, Calvindoro Satyagraha, Vinson Ciawandy
   TODO: include typing for function outputs
"""

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
from pytz import timezone
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
tqdm.pandas()
import gc
import inspect
import logging
import math
import numpy as np
import pandas as pd

# ema
def ema(xs, discounts, factor, asc=True):
    """
    xs: data/series in form of numpy array
    discounts: discount array
    factor: discount factor
    asc: ascending or descending
    """
    import numpy as np
    
    assert isinstance(xs,np.ndarray)
    assert isinstance(discounts,np.ndarray)
    assert isinstance(factor,float)

    ##################### NEW #####################
    if np.isinf(factor) and np.sign(factor) == -1:
        asc = asc == False # negate the asc
        factor = np.inf
    ###############################################

    _dcnt = discounts.copy()
    if not asc: # descending means from left to right, the effect decreases
        # while ascending increase effects to the right instead of left
        _dcnt = 1 - _dcnt
    e_dcnt = _dcnt*factor
    nan_locs = np.isnan(e_dcnt)
    if sum(nan_locs):
        e_dcnt[nan_locs] = 0
    ws = np.exp(-e_dcnt) # the higher the minus the smaller the value
    return np.matmul(xs, ws) / sum(ws) # ema weighted

class AbstractProcessor(ABC):
    @abstractmethod
    def __init__(self, params: dict={}):
        self.params = params
    
    @abstractmethod
    def fit(self, X, y = None):
        pass
    
    @abstractmethod
    def transform(self, X):
        pass
    
    @abstractmethod
    def fit_transform(self, X, y = None):
        pass

# ### inverse_transform explanation
# - remove_leading_zero is almost impossible to be inverted as we dunno how many leading zeros to return once it's been removed.
# - generate_missing_dates is almost impossible to be inverted as we dunno which one is the original dates or missing dates if we dont flag from the beginning.
# - fill missing value is also impossible because when the empty value has been filled, everything looks the same between the one that was originally empty and the one that has been filled at first.
# - add mapped column is a little bit impossible without save the original copy

class RoundingProcessor(BaseEstimator, TransformerMixin):
    def __init__(self, params: dict={}):
        self.method = params.get('method', '') # '': round, up: ceil, down: floor
        self.force = params.get('force', False)
        self.params = params
        
    def fit(self, X: pd.DataFrame, y = None):
        self.columns = []
        self.dtypes = []
        X = X.copy()
        for column in X.columns:
            if X[column].dtype == float:
                ### any change must be reverted back
                X.loc[:, column] = X[column].fillna(0) # make sure all value are filled otherwise will get IntCastingNaNError
                X.loc[:, f'{column}_int'] = X[column].astype(int)
                ###
                if X[f'{column}_int'].sum() == X[column].sum():
                    self.dtypes.append(int)
                else:
                    self.dtypes.append(float)
            else:
                self.dtypes.append(X[column].dtype)
            self.columns.append(column)
        return self
    
    def transform(self, X: pd.DataFrame): # dataframe of one column
        if self.method == 'up':
            fn = np.ceil
        elif self.method == 'down':
            fn = np.floor
        else: # ''
            fn = np.round
        
        for column, dtype in zip(self.columns, self.dtypes):
            if dtype not in [bool, int, float]: # 16, 32, 64
                import warnings
                msg = f"doesn\'t support rounding {dtype} data type!!"
                warnings.warn(msg)
                pass
            else:
                logging.info(f'round: (column: {column}, dtype: {dtype})')
                m = X[column].notna()
                X.loc[m, column] = fn(X.loc[m, column]).astype(int if self.force else dtype)
            
        return X
    
    def fit_transform(self, X: pd.DataFrame, y = None):
        return self.fit(X, y).transform(X)

# remove leading zero
class LeadingZeroProcessor(BaseEstimator, TransformerMixin):
    def __init__(self, params: dict={}):
        self.date_column = params['date_column']
        self.group_key = params['group_key'] # id
        self.forecast_column = params['forecast_column']
        self.params = params
        
    def fit(self, X: pd.DataFrame, y = None):
        return self
    
    def transform(self, X: pd.DataFrame):
        X_c = X.sort_values(by=self.group_key + [self.date_column], ascending=True, ignore_index=True)
        X_c.loc[:, self.forecast_column] = X_c[self.forecast_column].fillna(0)
        return X_c[X_c.groupby(self.group_key)[self.forecast_column].cumsum().gt(0)]
    
    def fit_transform(self, X: pd.DataFrame, y = None):
        return self.fit(X, y).transform(X)

# generate missing dates
class MissingDateProcessor(BaseEstimator, TransformerMixin):
    def __init__(self, params: dict={}):
        self.date_column = params['date_column']
        self.group_key = params['group_key'] # id
        self.n_days_ahead = params.get('n_days_ahead', 0)
        self.params = params

    def fit(self, X, y = None):
        try:
            self.date_max = X[self.date_column].max() + pd.DateOffset(days=self.n_days_ahead)
        except:
            X.loc[:, self.date_column] = pd.to_datetime(X[self.date_column])
            self.date_max = X[self.date_column].max() + pd.DateOffset(days=self.n_days_ahead)
        return self

    def transform(self, X):
        df = X.groupby(self.group_key)[self.date_column].min().reset_index(self.group_key)
        df.columns = self.group_key + [f'{self.date_column}_min'] # rename column date_key to date_key_min
        df[f'{self.date_column}_max'] = self.date_max # just 1 copy - take latest date exist on the data
        # Generate missing dates
        df[self.date_column] = df.apply(
            lambda r: pd.date_range(r[f'{self.date_column}_min'], r[f'{self.date_column}_max']), axis=1
        )
        # convert list of pd.Series then stack it
        df = df.explode(self.date_column).reset_index(drop=True)
            
        try:
            return pd.merge(
                left=df[df.columns.difference([f'{self.date_column}_min', f'{self.date_column}_max'])], 
                right=X,
                on=self.group_key + [self.date_column], 
                how='left'
            )
        except:
            X.loc[:, self.date_column] = pd.to_datetime(X[self.date_column])
            return pd.merge(
                left=df[df.columns.difference([f'{self.date_column}_min', f'{self.date_column}_max'])], 
                right=X,
                on=self.group_key + [self.date_column], 
                how='left'
            )

    def fit_transform(self, X, y = None):
        return self.fit(X, y).transform(X)

class NormalizeProcessor(AbstractProcessor):
    from sklearn.preprocessing import Normalizer
    # normalization refers to a per sample transformation instead of a per feature transformation
    def __init__(self, params: dict={}):
        norm = params.get('norm', 'l2')
        copy = params.get('copy', True)
        self.obj = NormalizeProcessor.Normalizer(norm=norm, copy=copy)

    def fit(self, X):
        self.columns = X.columns
        self.obj.fit(X)

    def transform(self, X):
        result =  self.obj.transform(X)
        return pd.DataFrame(data=result, columns=self.columns)

    def fit_transform(self, X):
        return self.obj.fit_transform(X)

class StandardProcessor(BaseEstimator, TransformerMixin):
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
    def __init__(self, params: dict={}):
        copy = params.get('copy', True)
        with_mean = params.get('with_mean', True)
        with_std = params.get('with_std', True)
        self.obj = StandardScaler(copy=copy, with_mean=with_mean, with_std=with_std)
        self.params = params
        
    def fit(self, X, y = None):
        self.obj.fit(X, y)
        property_attrs = {
            'scale_': self.obj.scale_,
            'mean_': self.obj.mean_,
            'var_': self.obj.var_,
            'n_features_in_': self.obj.n_features_in_,
            'feature_names_in_': self.obj.n_features_in_,
            'n_samples_seen_': self.obj.n_samples_seen_,
        }
        for name, value in property_attrs.items():
            # object - attribute name - value
            setattr(self.__class__, name, value)
        return self
    
    def transform(self, X):
        return self.obj.transform(X)
    
    def fit_transform(self, X, y = None):
        return self.fit(X, y).transform(X)

class MinMaxProcessor(BaseEstimator, TransformerMixin):
    def __init__(self, params: dict={}):
        feature_range = params.get('feature_range', (0, 1))
        copy = params.get('copy', True)
        self.obj = MinMaxScaler(feature_range=feature_range, copy=copy)
        self.params = params
        
    def fit(self, X, y = None):
        self.obj.fit(X, y)
        property_attrs = {
            'min_': self.obj.min_,
            'scale_': self.obj.scale_,
            'data_min_': self.obj.data_min_,
            'data_max_': self.obj.data_max_,
            'data_range_': self.obj.data_range_,
            'n_samples_seen_': self.obj.n_samples_seen_,
            'feature_names_in_': self.obj.feature_names_in_,
        }
        for name, value in property_attrs.items():
            # object - attribute name - value
            setattr(self.__class__, name, value)
        return self

    def transform(self, X):
        return self.obj.transform(X)
    
    def fit_transform(self, X, y = None):
        return self.fit(X, y).transform(X)

class RobustProcessor(BaseEstimator, TransformerMixin):
    '''Removes the median and scales the data according to the quantile range (defaults to IQR: Interquartile Range). 
    The IQR is the range between the 1st quartile (25th quantile) and the 3rd quartile (75th quantile).
    Centering and scaling happen independently on each feature by computing the relevant statistics on the samples 
    in the training set. Median and interquartile range are then stored to be used on later data using the transform method. 
        
    Standardization of a dataset is a common requirement for many machine learning estimators. 
    Typically this is done by removing the mean and scaling to unit variance. 
    However, outliers can often influence the sample mean / variance in a negative way. 
    In such cases, the median and the interquartile range often give better results
    '''
    def __init__(self, params: dict={}):
        with_centering = params.get('with_centering', True)
        with_scaling = params.get('with_scaling', True)
        quantile_range = params.get('quantile_range', (25.0, 75.0))
        copy = params.get('copy', True)
        unit_variance = params.get('unit_variance', False)
        self.obj = RobustScaler(
            with_centering=with_centering, 
            with_scaling=with_scaling, 
            quantile_range=quantile_range,
            copy=copy,
            unit_variance=unit_variance,
        )
        self.params = params
        
    def fit(self, X, y = None):
        self.obj.fit(X, y)
        property_attrs = {
            'center_': self.obj.center_, # The median value for each feature in the training set
            'scale_': self.obj.scale_, # The (scaled) interquartile range for each feature in the training set
            'feature_names_in_': self.obj.feature_names_in_,
        }
        for name, value in property_attrs.items():
            # object - attribute name - value
            setattr(self.__class__, name, value)
        return self
    
    def transform(self, X):
        return self.obj.transform(X)
    
    def fit_transform(self, X, y = None):
        return self.fit(X, y).transform(X)

class PowerProcessor(BaseEstimator, TransformerMixin):
    '''
    Apply a power transform featurewise to make data more Gaussian-like.
    Power transforms are a family of parametric, monotonic transformations that are applied to make data more Gaussian-like. 
    This is useful for modeling issues related to heteroscedasticity (non-constant variance), 
    or other situations where normality is desired.
    Currently, PowerTransformer supports the Box-Cox transform and the Yeo-Johnson transform. 
    The optimal parameter for stabilizing variance and minimizing skewness is estimated through maximum likelihood.
    Box-Cox requires input data to be strictly positive, while Yeo-Johnson supports both positive or negative data.
    By default, zero-mean, unit-variance normalization is applied to the transformed data.
    '''
    def __init__(self, params: dict={}):
        method = params.get('method', 'yeo-johnson')
        standardize = params.get('standardize', True)
        copy = params.get('copy', True)
        self.obj = PowerTransformer(method=method, standardize=standardize, copy=copy)
        self.params = params
        
    def fit(self, X, y = None):
        self.obj.fit(X, y)
        property_attrs = {
            'lambdas_': self.obj.lambdas_,
            'feature_names_in_': self.obj.feature_names_in_,
        }
        for name, value in property_attrs.items():
            # object - attribute name - value
            setattr(self.__class__, name, value)
        return self
    
    def transform(self, X):
        return self.obj.transform(X)
    
    def fit_transform(self, X, y = None):
        return self.fit(X, y).transform(X)

def custom_quantile_in(X: pd.DataFrame, ma: int=0, orient: int=1): # column
    if orient:
        ma += 1 if ma > 0 else 0
        X = X.dropna().iloc[:, -ma:-1]
        q1 = math.floor(0.25 * len(X.columns))
        q3 = math.ceil(0.75 * len(X.columns))
        x = X.iloc[:, q1:q3]# .take([q1, q3])
    else:
        X = X.dropna().iloc[-ma:]
        q1 = math.floor(0.25 * len(X))
        q3 = math.ceil(0.75 * len(X))
        x = X.iloc[q1:q3]
    return x.mean(axis=orient)

def custom_quantile_ex(X: pd.DataFrame, ma: int=0, orient: int=1):
    if orient:
        ma += 1 if ma > 0 else 0
        x = X.iloc[:, -ma:].fillna(1)
    else:
        x = X.dropna().iloc[-ma:]
    q13 = x.quantile(q=[0.25, 0.75], axis=orient)
    result = q13.mean()
    return result

def custom_min_max(X: pd.DataFrame, ma: int=0, orient: int=1):
    if orient:
        ma += 1 if ma > 0 else 0
        x = X.iloc[:, -ma:].fillna(1)
    else:
        x = X.dropna().iloc[-ma:]
    q04 = x.quantile(q=[0, 1], axis=orient)
    result = q04.mean()
    return result

def custom_shift(X: pd.DataFrame, ma: int=0, orient: int=1):
    if orient:
        ma += 1 if ma > 0 else 0
        X_used = X.iloc[:, -ma:-1].fillna(1)
    else:
        X_used = X.dropna().iloc[-ma:].T
    weights = np.arange(len(X_used.columns), dtype=np.float32) + 1
    weights /= sum(weights)
    return X_used.dot(weights)

def custom_mean(X: pd.DataFrame, ma: int=0, orient: int=1):
    if orient: # columns
        ma += 1 if ma > 0 else 0
        x = X.iloc[:, -ma:-1]
    else: # rows
        x = X.dropna().iloc[-ma:]
    return x.mean(axis=orient)

def custom_median(X: pd.DataFrame, ma: int=0, orient: int=1):
    if orient: # columns
        ma += 1 if ma > 0 else 0
        x = X.dropna().iloc[:, -ma:-1]
    else: # rows
        x = X.dropna().iloc[-ma:]
    return x.median(axis=orient)

def custom_ema(X: pd.DataFrame, ma: int=0, magnitude: int=0, orient: int=1):
    """fill the value of last item with exponential moving average.
    Is_Impute_Include: do we stand on the data to be imputed / whether we use the data to be imputed as the last item"""
    try:
        if orient:
            ma += 1 if ma > 0 else 0
            X_used = X.iloc[:, -ma:-1].fillna(1)# take out the last column as it's the one that we'll impute
            Is_Impute_Include = False
        else: # 0
            X_used = X.dropna().iloc[-ma:].T
            Is_Impute_Include = True
        days = len(X_used.columns)
        discounts = (np.arange(days) + (1 - int(Is_Impute_Include))) / float(days - int(Is_Impute_Include))
        assert days > 1
    except (AssertionError, ZeroDivisionError) as e: # scalar
        result = 1 if X_used.empty else X_used.squeeze()# to avoid empty series
        return result
    else:
        return X_used.apply(func=lambda x: ema(x.to_numpy(), discounts, magnitude), axis=1)

class FillMissingProcessor(BaseEstimator, TransformerMixin):
    """Fill missing values with one of these methods:
    01. mean,
    02. median,
    03. mode,
    04. '': constant,
    05. bfill / backfill
    06. ffill / pad
    07. interpolation - linear
    08. repeat
    09. random sampling
    10. shift
    11. ema
    """

    def impute(df: pd.DataFrame, key_col: str, date_col: str, val_col: object, fn: object):
        cols_original_order = df.columns
        unused_cols = set(cols_original_order)# - set([key_col,date_col])

        if isinstance(val_col,list):
            unused_cols -= set(val_col)
        else :
            unused_cols -= set([val_col])

        unused_df = df[unused_cols]

        original_date_range = df.groupby(key_col).agg({date_col:['min','max']}).droplevel(axis=1,level=0)
        df_pivot = df.melt(value_vars = val_col,id_vars = [key_col,date_col]).pivot_table(
            index=[key_col,'variable'],
            columns=[date_col],
            values='value',
            dropna=False
        )
        first_col = df_pivot.columns[0] # All the average calculation will anchored to the first date.
        for col in tqdm(df_pivot.columns[1:], desc=val_col) : # iterate over date column => to the right
            temp = df_pivot.loc[:,first_col:col]
            new_values = fn(temp) # must be 2d (row: product_id * warehouse_id ; column: date_key)
            df_pivot[col] = df_pivot[col].fillna(new_values)# temp.mean(axis=1))
        df = df_pivot.melt(ignore_index=False) # original index is retained
        df = df.reset_index().pivot( # get the index and re-arrange the table
            index=[key_col,date_col],
            columns='variable',
            values='value'
        )
        df = df.reset_index(level=1) # put back the date_key as column

        # # Remove unnecessary date
        df = df.join(original_date_range) # on key_col
        df = df[df[date_col].between(df['min'],df['max'])].drop(columns=['min','max'])
        # Date where missing happens from start is still there, so fill it with zero
        df[val_col]=df[val_col].fillna(0)

        del df_pivot, original_date_range # free some memory

        # return it to original form
        # df = pd.concat([df.reset_index(),unused_df],axis=1).loc[:,cols_original_order]
        df = pd.merge(left=unused_df, right=df.reset_index(), on=[key_col,date_col], how='left').loc[:,cols_original_order]

        return df

    def __init__(self, params: dict={}):
        self.method = params.get('method', '')
        try:
            self.method in ['mean', 'median', 'mode', '', 'bfill', 'ffill', 'repeat', 'random', 'shift', 
                            'ema_past', 'ema_recent', 'linear']
        except:
            import warnings
            warnings.warn(f"method {self.method} is invalid would be reset to \'\'")
            self.method = ''
        self.lookup = params.get('lookup', 0)
        self.groupby = params.get('groupby', None)
        self.column = params.get('column', None)
        self.options = params.get('options', {})
        self.params = params
        
    def fit(self, X, y = None):

        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
        elif isinstance(X, pd.DataFrame):
            pass
        else:
            import warnings
            warnings.warn("X to be fitted on must either pandas dataframe or numpy array")

        self.original_columns = X.columns

        if self.column: # not empty
            return self # just get out, calculation will be done on transform function instead of here

        # else define lookup table
        if self.method == 'mean':
            self.lookup = X.mean()
        elif self.method == 'quantile_ex':
            self.lookup = X.quantile([.25, .75]).mean()
        elif self.method == 'min_max':
            self.lookup = X.quantile([0, 1]).mean()
        elif self.method == 'quantile_in':
            q1 = int(0.25 * len(X))
            q3 = int(0.75 * len(X)) + 1
            self.lookup = X[q1:q3].mean()
        elif self.method == 'median':
            self.lookup = X.median()
        elif self.method == 'mode':
            self.lookup = X.mode(axis=0).iloc[0] # take the 1st row
        elif self.method == 'linear':
            self.lookup = X.interpolate().iloc[-1] # take the last row
        elif self.method == 'random':
            self.lookup = X

        return self
    
    def transform(self, X):
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
        elif isinstance(X, pd.DataFrame):
            pass
        else:
            import warnings
            warnings.warn("X to transform must either pandas dataframe or numpy array")

        if self.column: # not empty
            if self.method == 'mean':
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                if self.options.get('step', 'sequential') == 'sequential':
                    mean_adapter = lambda x: custom_mean(x, self.options.get('ma', 0))
                    X = FillMissingProcessor.impute(df=X, key_col='FILL_ID',
                                                    date_col=self.options.get('update', 'date_key'),
                                                    val_col=self.column, fn=mean_adapter)
                else:
                    mean_adapter = lambda x: custom_mean(X=x.to_frame(),#x is pd.Series
                                                         ma=self.options.get('ma', 0), 
                                                         orient=0) # date_key as index
                    self.lookup = X.groupby(['FILL_ID'])[self.column].agg(mean_adapter).fillna(0)
                    X[self.column] = X.set_index('FILL_ID')[self.column].fillna(self.lookup).values # just take out the value
            elif self.method == 'quantile_ex':
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                if self.options.get('step', 'sequential') == 'sequential':
                    # custom_quantile_ex = lambda x: x.quantile(q=[0.25, 0.75], axis=1).mean(axis=1) # Q1 and Q3
                    quantile_ex_adapter = lambda x: custom_quantile_ex(x, self.options.get('ma', 0))
                    X = FillMissingProcessor.impute(df=X, key_col='FILL_ID',
                                                    date_col=self.options.get('update', 'date_key'),
                                                    val_col=self.column, fn=quantile_ex_adapter)
                else:
                    # quantile([0.25, 0.75]).mean()
                    quantile_ex_adapter = lambda x: custom_quantile_ex(X=x.to_frame(),
                                                                       ma=self.options.get('ma', 0), 
                                                                       orient=0)
                    self.lookup = X.groupby(['FILL_ID'])[self.column].agg(quantile_ex_adapter).fillna(0)
                    X[self.column] = X.set_index('FILL_ID')[self.column].fillna(self.lookup).values # index must be removed
            elif self.method == 'min_max':
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                if self.options.get('step', 'sequential') == 'sequential':
                    min_max_adapter = lambda x: custom_min_max(x, self.options.get('ma', 0))
                    X = FillMissingProcessor.impute(df=X, key_col='FILL_ID',
                                                    date_col=self.options.get('update', 'date_key'),
                                                    val_col=self.column, fn=min_max_adapter)
                else:
                    # quantile([0.25, 0.75]).mean()
                    min_max_adapter = lambda x: custom_min_max(X=x.to_frame(),
                                                                       ma=self.options.get('ma', 0), 
                                                                       orient=0)
                    self.lookup = X.groupby(['FILL_ID'])[self.column].agg(min_max_adapter).fillna(0)
                    X[self.column] = X.set_index('FILL_ID')[self.column].fillna(self.lookup).values # index must be removed
            elif self.method == 'quantile_in':
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                if self.options.get('step', 'sequential') == 'sequential':
                    quantile_in_adapter = lambda x: custom_quantile_in(x, self.options.get('ma', 0))
                    X = FillMissingProcessor.impute(df=X, key_col='FILL_ID',
                                                    date_col=self.options.get('update', 'date_key'),
                                                    val_col=self.column, fn=quantile_in_adapter)
                else:
                    quantile_in_adapter = lambda x: custom_quantile_in(X=x.to_frame(), 
                                                                       ma=self.options.get('ma', 0), 
                                                                       orient=0)
                    self.lookup = X.groupby(['FILL_ID'])[self.column].agg(quantile_in_adapter).fillna(0)
                    X[self.column] = X.set_index('FILL_ID')[self.column].fillna(self.lookup).values
            elif self.method == 'median':
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                if self.options.get('step', 'sequential') == 'sequential':
                    median_adapter = lambda x: custom_median(x, self.options.get('ma', 0))
                    X = FillMissingProcessor.impute(df=X, key_col='FILL_ID',
                                                    date_col=self.options.get('update', 'date_key'),
                                                    val_col=self.column, fn=median_adapter)
                else:
                    median_adapter = lambda x: custom_median(X=x.to_frame(), 
                                                             ma=self.options.get('ma', 0), 
                                                             orient=0)
                    self.lookup = X.groupby(['FILL_ID'])[self.column].agg(median_adapter).fillna(0)
                    X[self.column] = X.set_index('FILL_ID')[self.column].fillna(self.lookup).values
            elif self.method == 'linear':
                self.lookup = X.groupby(self.groupby)[self.column].apply(lambda x : x.interpolate(method='linear')).fillna(0)
                X[self.column] = X[self.column].fillna(self.lookup)
            elif self.method == 'repeat':
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                X.loc[X[self.column].notna(), 'no_item'] = X[X[self.column].notna()].groupby('FILL_ID').cumcount()
                X.loc[X[self.column].isna(), 'no_item'] = X[X[self.column].isna()].groupby('FILL_ID').cumcount()
                self.lookup = X[X[self.column].notna()].groupby('FILL_ID').tail(3) # take the last 3 records from each group
                self.lookup['no_item'] = self.lookup.groupby('FILL_ID').cumcount()
                self.lookup['FILL_ID_2'] = self.lookup['FILL_ID'] + '#' + self.lookup['no_item'].astype(int).astype(str)
                self.lookup.set_index('FILL_ID_2', inplace=True)
                X['FILL_ID_2'] = X['FILL_ID'] + '#' + X['no_item'].astype(int).astype(str)
                X[self.column] = X[self.column].fillna(X['FILL_ID_2'].map(self.lookup[self.column])).fillna(0)
            elif self.method == '': # constant
                X[self.column] = X[self.column].fillna(self.lookup)
            elif self.method == 'shift':
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                if self.options.get('step', 'sequential') == 'sequential':
                    shift_adapter = lambda x: custom_shift(x, self.options.get('ma', 0))
                    X = FillMissingProcessor.impute(df=X, key_col='FILL_ID',
                                                    date_col=self.options.get('update', 'date_key'),
                                                    val_col=self.column, fn=shift_adapter)
                else:
                    shift_adapter = lambda x: custom_shift(X=x.to_frame(), # series to dataframe 
                                                           ma=self.options.get('ma', 0), 
                                                           orient=0) # and also data arranged vertically (top-down)
                    self.lookup = X.groupby(['FILL_ID'])[self.column].agg(shift_adapter).fillna(0)
                    X[self.column] = X.set_index('FILL_ID')[self.column].fillna(self.lookup).values
            elif self.method.startswith('ema'): # either ema_past or ema_recent
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                magnitude = -2. if self.method == 'ema_past' else +2. # otherwise ema recent
                if self.options.get('step', 'sequential') == 'sequential':
                    ema_adapter = lambda x: custom_ema(x, self.options.get('ma', 0), magnitude)
                    X = FillMissingProcessor.impute(df=X, key_col='FILL_ID',
                                                    date_col=self.options.get('update', 'date_key'),
                                                    val_col=self.column, fn=ema_adapter)
                else:
                    ema_adapter = lambda x: custom_ema(X=x.to_frame(), 
                                                       ma=self.options.get('ma', 0),
                                                       magnitude=magnitude, orient=0)
                    self.lookup = X.groupby(['FILL_ID'])[self.column].agg(ema_adapter).fillna(0)
                    X[self.column] = X.set_index('FILL_ID')[self.column].fillna(self.lookup).values
            elif self.method in ['bfill', 'ffill']:
                X['FILL_ID'] = X.apply(lambda r: '#'.join([str(r[c]) for c in self.groupby]), axis=1)
                if self.method == 'ffill':
                    X[self.column] = X.groupby('FILL_ID')[self.column].transform(lambda v: v.ffill())
                else:
                    X[self.column] = X.groupby('FILL_ID')[self.column].transform(lambda v: v.bfill())
        else:
            if self.method in ['bfill', 'ffill']:
                return X.fillna(method=self.method)
            elif self.method in ['', 'mean', 'median', 'mode', 'linear', 'quantile_ex', 'quantile_in', 'min_max']:
                return X.fillna(value=self.lookup)
            elif self.method == 'random':
                for c in X.columns:
                    na = X[c].isna() # boolean mask
                    n = na.sum() # sample size
                    if n > 0:
                        X.loc[na, c] = self.lookup.loc[self.lookup[c].notna(), c].sample(n=n).values
                return X
        return X[self.original_columns] # only return the original columns
        
    def fit_transform(self, X, y = None):
        # super().fit_transform(X, y)
        return self.fit(X, y).transform(X)
        # pass

class AddingColumnProcessor(BaseEstimator, TransformerMixin):
    def __init__(self, params: dict={}):
        self.src_column = params.get('src_column', None)
        self.dst_column = params['dst_column']
        self.fn = params['fn']
        self.params = params
        
    def fit(self, X: pd.DataFrame, y = None):
        return self
    
    def transform(self, X: pd.DataFrame):
        X.loc[:, self.dst_column] = X[self.src_column].map(self.fn)
        if self.src_column:
            return X # dataframe
        else:
            return X[self.dst_column] # series
        
    def fit_transform(self, X, y = None):
        return self.fit(X, y).transform(X)

class PreprocessFactory():
    preprocess_menu = {
        'generate_missing_dates': MissingDateProcessor,
        'remove_leading_zero': LeadingZeroProcessor,
        'normalization': NormalizeProcessor,
        'standardization': StandardProcessor,
        'fill_missing': FillMissingProcessor,
        'min_max_scaling': MinMaxProcessor,
        'robust_scaling': RobustProcessor,
        'power_transform': PowerProcessor,
        'add_mapped_column': AddingColumnProcessor,
        'post_round': RoundingProcessor,
    }
    def __init__(self, preprocess_steps: dict={}):
        self.column_orders = []
        self.preprocess_orders = []
        
        self.pipe = {};
        self.steps = {};
        for c in preprocess_steps:
            self.steps[c] = []
            for p in preprocess_steps[c]:
                menu = PreprocessFactory.preprocess_menu[p]
                params = preprocess_steps[c][p].get('params', [preprocess_steps[c][p]])
                size = preprocess_steps[c][p].get('size', len(params))
                for i in range(size):
                    param = params[i]
                    self.steps[c].append((f"{p}_{i}_{c if c else 'all'}", menu(param)))

                    #### backup section
                    self.preprocess_orders.append(menu(param))
                    self.column_orders.append(c)
                    #### end section
            self.pipe[c] = Pipeline(steps=self.steps[c])

    def fit(self, X):
        """save the original data.
        fit the data to each step / object in pipeline
        """
        self.X_ori = X.copy()
        for k in self.pipe:
            if k:
                self.pipe[k].fit(X[[k]])
            else:
                self.pipe[k].fit(X)
        return self

    def transform(self, X):
        """Transform the data, and apply transform with the final estimator."""
        for k in self.pipe:
            if k:
                X.loc[:, k] = self.pipe[k].transform(X[[k]])
            else:
                X = self.pipe[k].transform(X)
        return X

    def fit_transform(self, X, y = None):
        """Fit the model and transform with the final estimator."""
        # return self.fit(X, y).transform(X)
        for k in self.pipe:
            if k:
                X.loc[:, k] = self.pipe[k].fit_transform(X[[k]])
            else:
                X = self.pipe[k].fit_transform(X)
        return X

    #### would be deprecated ####
    def execute(self, X):
        df = X.copy()
        for i in range(len(self.preprocess_orders)):
            c = self.column_orders[i]
            if c: # c is not empty '' means specified column
                self.preprocess_orders[i].fit(df[[c]])
                df.loc[:, c] = self.preprocess_orders[i].transform(df[[c]])
            else:
                self.preprocess_orders[i].fit(df)
                df = self.preprocess_orders[i].transform(df)
        return df
