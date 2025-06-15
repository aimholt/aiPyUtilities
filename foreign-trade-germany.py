import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from aipy.pd_extensions import df_col_check

### reading dataset to DF
df=pd.read_csv('TestData\\aussenhandel_deutschland.csv',sep=';', decimal=',')

COUNTRY='Vereinigte Staaten von Amerika'
TYPE='Einfuhr: Wert'

#renaming columns
df.rename(columns={
				'time':                         'year',
				'1_variable_attribute_label':   'month',
				'3_variable_attribute_label':   'country',
				'1_variable_attribute_code':    'MCode',
				'value_variable_label':         'type',
				'value_unit':                   'unit',
                }, inplace=True)
### making sorted list of types, countries and years
df_types=df['type'].unique().tolist()
df_types.sort()
df_countries=df['country'].unique().tolist()
df_countries.sort()
df_years=df['year'].unique().tolist()
df_years.sort()
colors=['pink','cyan','green','yellow','blue','red']
plt.figure(figsize=(10, 5), layout='constrained',)
plt.ticklabel_format(style='plain')
for type in df_types:
	if type.find('US-Dollar') >= 0:
		print(">>>",type)
		xdf=df[['year','month','value']] \
			[
			(df['type'] == type) & 
			(df['country'] == COUNTRY)
			]
		xdf['month']=df['MCode'].str.strip('MONAT')
		xdf['date']=pd.to_datetime(xdf[['year','month']].assign(day=1))
		xdf.sort_values('date', inplace=True)
		xdf['value']=xdf['value'].replace('...',np.nan)
		xdf['value']=xdf['value'].replace('-',np.nan)
		xdf['value'].dropna(inplace=True)
		xdf=xdf[xdf['value'].notna()]
		xdf['value']=xdf['value'].astype(np.int64)
		plt.plot('date','value',data=xdf,color=colors.pop(),label=type)
plt.title('Außenhandel \nDeutschland - '+COUNTRY)
plt.xlabel('Zeit')
plt.ylabel('Wert (Tsd USD)')
plt.legend() 
plt.grid(True)
plt.tight_layout()
plt.show()