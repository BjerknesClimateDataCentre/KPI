###############################################################################
### KPI: Bat plot(s)                                                        ###
###############################################################################

### Description:
# The output plot will give an overview of how many flags of each type for
# each parameter of interest.

#------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd


def bar_plot(colnames, df, output_dir):

	label = []
	value = []
	for colname in colnames:
		colname = colname + ' QC Flag'

		add_to_label = [colname]*len(df[colname])
		label = label + add_to_label

		add_to_value = list(df[colname])
		value = value + add_to_value

	new_df = pd.DataFrame({'labels': label, 'values': value})

	f, ax = plt.subplots(figsize=(12,7))
	ax = sns.barplot(data=new_df, x='labels', y='values', estimator=len, hue='values')

	filename = 'bar_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')


	#df_fco2 = df[colname[1]]
	#print(type(df_fco2))
	#print(df_fco2[0:150,])

	return filename