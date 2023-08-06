"""
Author:
   Alan Choon, Anthony Jaya, Calvindoro Satyagraha
"""
import os
import pandas as pd
from typing import List
from pathlib import Path

def anti_join(x: pd.DataFrame, y: pd.DataFrame, on: List[str]) -> pd.DataFrame:
    '''
    Returns a dataframe containing records present in x but not in y
        Parameters:
            1. x: A pandas Dataframe
            2. y: Another pandas Dataframe

        Returns:
            df (pd.DataFrame): Dataframe containing results present in x but not in y
    '''
    ans = pd.merge(left=x[on], right=y[on], how='left', indicator=True, on=on)
    ans = ans.loc[ans._merge == 'left_only', :].drop(columns='_merge')
    return ans

def read_text_from_file(text_file_dir: str, text_file_name: str) -> str:
    '''
    Returns a string that is from a text file
    Commonly used to read text from a sql file and convert that to python string
        Parameters:
            1. text_file_dir: Directory where text file is located
            2. text_file_name: Name of the text file with its extension (eg: query.sql)

        Returns:
            res: A string that is the text in the text file specified
    '''
    file_path = os.path.join(text_file_dir, text_file_name)
    return Path(file_path).read_text()