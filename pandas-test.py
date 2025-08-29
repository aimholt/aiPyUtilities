import pandas as pd
import numpy as np
import datetime

def gen_df():
    """
        generate a dataframe with a sample mix of data
    """
    list1=[2944,461,949,9525,1451,8876,7037,7793,7577,2189,951,5058,\
        9316,6851,4908,3482,1248,7894,5719,5778,9773,1084,4657,7465]
    list2=[1640,1855,7185,8136,6528,1808,5321,4102,8149,3938,3480,1310,\
        1991,4804,9278,7837,8962,5075,2515,5298,3168,7230,1368,8526]
    df = pd.DataFrame({
        "A": ["one", "one", "two", "three"] * 6,
        "B": ["A", "B", "C"] * 8,
        "C": ["foo", "foo", "foo", "bar", "bar", "bar"] * 4,
        "D": list1,     # using a list with fix values
        "E": list2,     # using a list with fix values
        "F": np.random.randint(0,10000,24), # using a list of random values 
        "G": np.random.randint(0,10000,24), # using a list of random values
        "H": [datetime.datetime(2023, i, 1) for i in range(1, 13)]+\
            [datetime.datetime(2023, i, 15) for i in range(1, 13)]
        })
    return df

def sample_pivot(df):
    """
        sample use of a pivot_table function
    """
    df=pd.pivot_table(
        df,                         # data in a pandas dataframe
        values=["D","E","F","G"],   # columns to aggregate
        index=["A", "B"],           # keys to group by on pivot table index
        columns=["C"],              # keys to group by on pivot table colums
        aggfunc=["sum"])            # function for aggregate(sum, mean, ...)
    return df

if __name__ == '__main__':
    df=gen_df()
    print(df.info())
    print(df.describe())
    print(df)
    print(sample_pivot(df))
