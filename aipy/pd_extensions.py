"""
    extensions for working with pandas dataframes
"""
import pandas as pd
def df_col_check(df:pd.DataFrame, diffvaluemax=12, printout=False):
    """
        returns a list with a dict for each column with
            - name
            - amount of different values in that column
            - list of different values (if < 12) 
    """
    col_infos= []
    for item in df.columns:
        value_list= []
        item_values=len(df[item].unique())
        if  0 < item_values <= diffvaluemax:
            for value in df[item].unique():
                value_list.append(value)
        else:
            value_list.append('::: (to long for printing)')
        col_infos.append({
            'name':         item,
            'values-count': item_values,
            'values-list':  value_list
            })

    if printout:
        for item in col_infos:    
            print('')
            print(f'name: {item['name']}')
            print(f'  > different values: {item['values-count']}:')
            for i in item['values-list']:
                print(f'    > {i}')
        return
    else:
        return col_infos
