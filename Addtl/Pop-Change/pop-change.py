# pop-change.py

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

project_dir = r'C:\\Users\\jerem\\OneDrive\\Documents\\School\\_REGIS\\2023-05_Summer\\MSDS670\\MSDS670\\Addtl\\Pop-Change\\'
data_dir = project_dir + r'data\\'
output_dir = project_dir + r'output\\'

df = pd.read_csv(data_dir + 'NST-EST2022-POPCHG2020_2022.csv')

print(df.columns)
print()
print(df.head())
print()
print(df)
df.drop(columns=['SUMLEV','REGION','DIVISION','NRANK_ESTBASE2020', 'NRANK_POPEST2020',
       'NRANK_POPEST2021', 'NRANK_POPEST2022', 'NRANK_NPCHG2020',
       'NRANK_NPCHG2021', 'NRANK_NPCHG2022', 'NRANK_PPCHG2020',
       'NRANK_PPCHG2021', 'NRANK_PPCHG2022'], axis=1, inplace=True)

print(df.columns)
print()
print(df.head())
print()
print(df)
print(df.info())

shape = gpd.read_file(data_dir + 'cb_2018_us_state_5m\\cb_2018_us_state_5m.shp')
print(shape.columns)
print(shape['NAME'].unique())

shape = pd.merge(left=shape, right=df, left_on='NAME', right_on='NAME', how='left')

print(shape.info())
shape = shape.dropna()
shape = shape[~shape['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
print(shape.info())

ax = shape.boundary.plot(edgecolor='black', linewidth=0.2, figsize=(20,10))
shape.plot(ax=ax, column='PPOPCHG_2022', legend=True, cmap='RdBu', legend_kwds={'shrink':0.3, 'orientation':'horizontal', 'format':'%.1f%%', 'label':'Population Change 2020-2022'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
for edge in ['left', 'right', 'top', 'bottom']:
    ax.spines[edge].set_visible(False)
ax.set_title('Population Change 2021-2022', size=20, weight='bold')
#plt.show()
plt.savefig(output_dir + 'pop-change.png', dpi=300, bbox_inches='tight')