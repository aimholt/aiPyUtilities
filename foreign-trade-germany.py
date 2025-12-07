from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from aiPyExtensions.pd_extensions import df_col_check
import os

### reading dataset to DF
df=pd.read_csv('TestData'+os.sep+'aussenhandel_deutschland.csv',sep=';', decimal=',')

countries=['Vereinigtes Königreich']
ccountries=[
            'Belgien (ab 1999)',
			'China',
			'Frankreich',
			'Italien',
			'Mexiko',
			'Spanien',
			'Vereinigtes Königreich',
			'Vereinigte Staaten von Amerika',
            'Vietnam',
            'Russische Föderation (ab 05/1992)'
        ]
type={
	'export':	'Ausfuhr: Wert (US-Dollar)',
	'import':	'Einfuhr: Wert (US-Dollar)'
	}
sample_y=True
show_import=True
show_export=True
show_saldo=True

curr_year=datetime.now().year

#renaming columns
df.rename(columns={
				'time':                         'year',
				'1_variable_attribute_label':   'month',
				'3_variable_attribute_label':   'country',
				'1_variable_attribute_code':    'MCode',
				'value_variable_label':         'type',
				'value_unit':                   'unit',
                }, inplace=True)
### making sorZted list of types, countries and years
df_countries=df['country'].unique().tolist()
df_countries.sort()
#for item in df_countries:
#    print(item)
df_years=df['year'].unique().tolist()
df_years.sort()


#fig, ax = plt.subplots()
plt.figure(figsize=(10, 5), layout='constrained',facecolor='lightgrey')
plt.ticklabel_format(axis='y', style='sci')

for country in countries:
	### df for each country including import and export
	print('processing: ', country)
	xdf=df[['country','year','month','value','type','MCode']] \
		[
			(df['country'] == country)	&
			(df['year'] != curr_year)	&
			((df['type'] == type['import']) | (df['type'] == type['export']))
		]
	xdf['value']=xdf['value'].replace('...',np.nan)
	xdf['value']=xdf['value'].replace('-',np.nan)
	xdf['value'].dropna(inplace=True)
	xdf=xdf[xdf['value'].notna()]
	xdf['value']=xdf['value'].astype(np.int64)
	### 
	xdf['month']=xdf['MCode'].str.strip('MONAT')
	xdf['date']=pd.to_datetime(xdf[['year','month']].assign(day=1))
	xdf.sort_values('date', inplace=True)
	xdf.set_index('date', inplace=True)
	### creating df with single row including export and import
	sdf=xdf[['country', 'year', 'month', 'value']][(xdf['type'] == type['export'])]
	sdf['import']=xdf['value'][(xdf['type'] == type['import'])]
	sdf.rename(columns={'value':'export'}, inplace=True)
	####
	if sample_y:
		sdf=sdf.resample('YE').sum(numeric_only=True)

	sdf=sdf.reset_index()

	if show_import:
		plt.plot('date','import',data=sdf,label=f'{country} (Importe)')
	if show_export:
		plt.plot('date','export',data=sdf,label=f'{country} (Exporte)')
	if show_saldo:
		sdf['saldo']=sdf['export']-sdf['import']
		plt.plot(
			'date',
			'saldo',
			data=sdf,
			label=f'{country} (saldo)',
			#width=1,
			#edgecolor="white",
			#linewidth=0.7,
			)
	#print(sdf)

plt.title('Außenhandel Deutschland')
plt.xlabel('Zeit')
plt.ylabel('Wert (Tsd. USD)')
plt.legend(title='legend', alignment='left',facecolor='lightgrey') 
plt.grid(True)
plt.tight_layout()
plt.show()