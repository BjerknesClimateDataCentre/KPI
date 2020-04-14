###############################################################################
### KPI: Bar plot(s)                                                        ###
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

# !!! Make stacked bars as an option !!! Is this possible in seaborn??

# !!! The bar plot does not look good when include more than 7 or so parameters,
# is it nessecary to fix, or simply always make stacked bars? (requires less
# space hence looks good even with many params)

# Function creates a barplot, saves the figure in the output directory, and
# returns the filename back to the main script.
def bar_plot(colnames, df, output_dir):

	# In order to create the barplot we need to create a new data frame
	# containing two columns: 'label' (containg the the parameter names), and
	# 'value' (contaning the QC flags).
	# First, create these columns as separate lists.
	label = []
	value = []
	for colname in colnames:
		# Remove the unit-part from the column name
		label_name = colname.split(" [")[0].replace(' ','\n')
		# The new label_name is added to the label list and needs to be
		# repeated as many times as there are measurements in df
		label = label + [label_name]*len(df[colname])

		# Store the name of the QC column in df
		flag_colname = colname + ' QC Flag'
		# Add the QC flags from the current column to the value list
		value = value + list(df[flag_colname])

	# Create the new dataframe with the two columns. Change missing numbers to
	# '999' to allow them to be counted and included in the barplot (as missing
	# data).
	new_df = pd.DataFrame({'label': label, 'value': value})
	new_df = new_df.fillna(999)

	# Define the figure size. (Width should be 1.5 times the number of
	# paramaters, however, minimum 3 and maximum 9.5.)
	width = sorted([3, 1.5*len(colnames), 9.5])[1]
	height = 4
	figsize = (width, height)

    # Create figure with barplot. ('estimator=len' means to plot the frequency
    # each flag occure; 'hue=value' means the value column is used for color
    # encoding)
	f, ax = plt.subplots(figsize=figsize)
	ax = sns.barplot(data=new_df, x='label', y='value', estimator=len,
		hue='value')

	# Edit the legend labels (words instead of the QC flag values)
	new_labels = ['Good', 'Questionable', 'Bad', 'Missing']
	h, l = ax.get_legend_handles_labels()
	ax.legend(h, new_labels, loc=0, title=False, fontsize=6)

	# Add axis labels
	plt.ylabel('Frequency')
	plt.xlabel('Parameter')

	# Save file
	filename = 'bar_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename