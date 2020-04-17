###############################################################################
### KPI: Bar plot(s)                                                        ###
###############################################################################

### Description:
# The output plot will give an overview of how many flags of each type for
# each parameter of interest.

#----------
# TODO:
# - Make stacked bars as an option !!! Is this possible in seaborn??
# - The bar plot does not look good when include more than 7 or so parameters,
# is it nessecary to fix, or simply always make stacked bars? (requires less
# space hence looks good even with many params)


#------------------------------------------------------------------------------
### Import packages

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd


#------------------------------------------------------------------------------
### Set variables

# Figure sizes
max_fig_width = 9.5
min_fig_width = 3
width_per_param = 1.5
fig_height = 4


#------------------------------------------------------------------------------
### Functions

# Function creates a barplot, saves the figure in the output directory, and
# returns the figures filename back to the main script.
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

	# Define the figure size. (Width depends on number of parameters, however,
	# there is a minimum and maximum width to take into account)
	fig_width = sorted([min_fig_width, width_per_param*len(colnames),
		max_fig_width])[1]
	figsize = (fig_width, fig_height)

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

def stacked_bar_plot(colnames, df, output_dir):

	# Create a list with unique flags assigned to the chosen parameters
	flag_list = []
	for colname in colnames:
		flag_colname = colname + ' QC Flag'
		unique_list = df[flag_colname].unique()
		for unique in unique_list:
			if unique not in flag_list:
				flag_list.append(unique)


	print(flag_list + ' has type' + type(flag_list))
	print(flag_list[0] + ' has type ' + type(flag_list[0]))
	print(flag_list[1] + ' has type ' + type(flag_list[1]))
	print(flag_list[2] + ' has type ' + type(flag_list[2]))
	print(flag_list[3] + ' has type ' + type(flag_list[3]))


	# Cleanup the flag list (replace NaN with Missing, and make numbers to int)
	for flag in flag_list:
		if type(flag) is str:
			flag_list[flag] = 'Missing'
			print(flag + "is a string")
		if type(flag) is float:
			flag_list[flag] = int(flag)
			print(flag + " is a float")

	print(flag_list)





	# Create one list per flag containing the number of flags per param






# EXAMPLE:
# y-axis in bold
#rc('font', weight='bold')

# Values of each group
#bars1 = [12, 28, 1, 8, 22]
#bars2 = [28, 7, 16, 4, 10]
#bars3 = [25, 3, 23, 25, 17]

# Heights of bars1 + bars2
#bars = np.add(bars1, bars2).tolist()

# The position of the bars on the x-axis
#r = [0,1,2,3,4]

# Names of group and bar width
#names = ['A','B','C','D','E']
#barWidth = 1

# Create brown bars
#plt.bar(r, bars1, color='#7f6d5f', edgecolor='white', width=barWidth)
# Create green bars (middle), on top of the firs ones
#plt.bar(r, bars2, bottom=bars1, color='#557f2d', edgecolor='white', width=barWidth)
# Create green bars (top)
#plt.bar(r, bars3, bottom=bars, color='#2d7f5e', edgecolor='white', width=barWidth)

# Custom X axis
#plt.xticks(r, names, fontweight='bold')
#plt.xlabel("group")
