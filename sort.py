import pandas as pd
import csv
import numpy as np
import rewrite

import __init__
from get_minmax import get_file
#-----open the file AAV for the range of items -mix ->max in the site (this including items already in the list and missing items)

df1 = get_file('aav.csv','aav.csv','AUTO AUCTIONS - SYDNEY')
df9 = get_file('all.csv','all.csv','ALLIANCE AUCTIONS - SYDNEY')
df10 = get_file('caa.csv','caa.csv','CARNET AUCTIONS')
df6 = get_file('cma.csv','cma.csv','CENTRAL AUTO AUCTIONS')
df3 = get_file('css.csv','css.csv','CARNET AUCTIONS - SMITHFIELD')
df4 = get_file('cty.csv','cty.csv','CITY MOTOR AUCTION')
df5 = get_file('f3a.csv','f3a.csv','F3 MOTOR AUCTIONS')
df7 = get_file('vma.csv','vma.csv','VALLEY MOTOR AUCTIONS - NEWCASTLE')
df8 = get_file('gma.csv','gma.csv','UNITED AUCTIONS NSW - LANE 1')
df2 = get_file('tma.csv','tma.csv','CARNET WESTERN SYDNEY')


#---------------Trimming Duplicates------------------

print('stocks aav',len(df1))
print('--------')
print('stocks tma',len(df2))
print('--------')
print('stocks css',len(df3))
print('--------')
print('stocks cty',len(df4))
print('--------')
print('stocks f3a',len(df5))
print('--------')
print('stocks cma',len(df6))
print('--------')
print('stocks vma',len(df7))
print('--------')
print('stocks gma',len(df8))
print('--------')
print('stocks all',len(df9))
print('--------')
print('stocks caa',len(df10))


#-------Combine all missing items------------

df0 = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10])
print('--------')

df0.drop_duplicates(subset=['link_stock'],keep="first",inplace=True)
df0.drop(['auction','status'], inplace=True, axis=1)
print('Total stocks:',len(df0))

#-------UPdate the missing dates------------

df0.to_csv(r'full.csv', index=False,encoding='utf-8')
