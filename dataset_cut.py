'''
Dataset cut
'''

import pandas as pd
import numpy as np

def read_dataset(path: str) -> pd.DataFrame:
    '''
    (str) -> pd.DataFrame
    Reads dataset
    '''
    df = pd.read_csv(
        path,
        sep = r'\t{1,10}',
        encoding = 'ISO-8859-1',
        skiprows = 15,
        names = ['Film', 'Location'],
        engine = 'python',
        index_col = False,
    )

    df[['Film', 'Year', 'Additional info']] =\
        df['Film'].str.extract(
        '^"?([^("]+)"?\s*\((\d+)\)\s*(.*)$',
        expand = True
    )

    del df['Additional info']

    df.to_csv(
        'data.csv',
        sep = ';',
        index = False
    )

    return df

def cut_dataset(path: str) -> pd.DataFrame:
    '''
    (str) -> pd.DataFrame
    Cuts dataset for optimal working time
    '''
    df = pd.read_csv(
        path,
        sep = ';',
        index_col = False
    )

    df.Film = np.where(
        df.Film.str.contains('¿', regex = True, na = False),
        None,
        df.Film
    )

    df.Location = np.where(
        df.Location.str.contains('¿', regex = True, na = False),
        None,
        df.Location
    )

    df.drop_duplicates(subset = ['Film'], inplace = True)
    df.drop_duplicates(subset = ['Location'], inplace = True)
    df.sort_values(by = ['Film', 'Year'])

    df.to_csv(
        'data_cut_test.csv',
        sep = ';',
        index = False
    )

    return df

if __name__ == '__main__':
    cut_dataset(read_dataset('locations.list'))