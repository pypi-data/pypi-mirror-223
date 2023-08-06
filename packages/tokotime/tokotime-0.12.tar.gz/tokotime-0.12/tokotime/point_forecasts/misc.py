import pandas as pd
import numpy as np
import datetime

def day_date_map(df, forecast_period, 
                 max_date,
                 output_date_col='forecast_date'):
    day_date_map = {i: max_date + datetime.timedelta(days=i+1) for i in range(forecast_period)}
    df[output_date_col] = df['day'].map(day_date_map)
    df.drop(columns=['day'], inplace=True)
    return df