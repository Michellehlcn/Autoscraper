import pandas as pd
import csv
import numpy as np
import operator


na_values = ["N/A",""]

#----------------------get min max for each site ------------------------

#----------------------get missing files and fill the empty columns ------------------------
def get_file(input,output,auction_site):
	
	df_input = pd.read_csv(f'{input}',keep_default_na=False, na_values=na_values)
	df_input.drop_duplicates(subset=['link_stock','build'],keep="first",inplace=True)
	df_input['auction_stock_site'] = df_input.link_stock.str.split('=', expand=True).apply(lambda x: (x[1]), axis=1)
	df_input['auction_stock_id'] = df_input.link_stock.str.split('=', expand=True).apply(lambda x: (x[2]), axis=1)
	df_input['auction_site'] = auction_site

	#-----Drop the label row (Alliance auction)-------
	df_input = df_input[df_input.make != 'Label']

	df_input.to_csv(f'{output}', index=False)
	return df_input