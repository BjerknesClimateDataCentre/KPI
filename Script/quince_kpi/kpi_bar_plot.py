###############################################################################
### KPI: Bar plot(s)                                                        ###
###############################################################################

### Description:
# The output plot will give an overview of how many flags of each type for
# each parameter of interest.


#------------------------------------------------------------------------------
### Import packages

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
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

# Width of bars in stacked bar plot
barWidth = 0.75

# Number of parameters which change a-axis label to vertical to avoid overlap
limit_nParameters = 8


#------------------------------------------------------------------------------
### Functions

# Define the figure size. Width depends on number of parameters, however,
# there is a minimum and maximum width to take into account.
def get_figsize(parameters):
	fig_width = sorted([min_fig_width, width_per_param*len(parameters),
		max_fig_width])[1]
	figsize = (fig_width, fig_height)
	return figsize


# Function creates a barplot, saves the figure in the output directory, and
# returns the figures filename back to the main script.
def bar_plot(parameters, df, output_dir):

	# In order to create the barplot we need to create a new data frame
	# containing two columns: 'label' (containg the the parameter names), and
	# 'value' (contaning the QC flags).
	# First, create these columns as separate lists.
	label = []
	value = []
	for parameter in parameters:
		# Remove the unit-part from the parameter name
		label_name = parameter.split(" [")[0].replace(' ','\n')
		# The new label_name is added to the label list and needs to be
		# repeated as many times as there are measurements in df
		label = label + [label_name]*len(df[parameter])

		# Store the name of the QC column in df
		flag_column = parameter + ' QC Flag'
		# Add the QC flags from the current column to the value list
		value = value + list(df[flag_column])

	# Create the new dataframe with the two columns. Change missing numbers to
	# '999' to allow them to be counted and included in the barplot (as missing
	# data).
	new_df = pd.DataFrame({'label': label, 'value': value})
	new_df = new_df.fillna(999)

	# Get the figsize
	figsize = get_figsize(parameters)

    # Create figure with barplot. ('estimator=len' means to plot the frequency
    # each flag occure; 'hue=value' means the value column is used for color
    # encoding)
	f, ax = plt.subplots(figsize=figsize)
	ax = sns.barplot(data=new_df, x='label', y='value', estimator=len,
		hue='value')

	# Edit the legend labels (words instead of the QC flag values)
	# !!! Make this part more generic !!!
	new_labels = ['Good', 'Questionable', 'Bad', 'Missing']
	h, l = ax.get_legend_handles_labels()
	ax.legend(h, new_labels, loc=0, title=False, fontsize=6)

	# Add axis labels
	plt.ylabel('Frequency')

	# Save file
	filename = 'bar_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename

# Function creates a stacked barplot, saves the figure in the output directory,
# and returns the figures filename back to the main script.
def stacked_bar_plot(parameters, df, output_dir, **kwargs):
	#---------
	# STRUCTURE DATA FOR PLOTTING
	# Create a list of unique flags given to the selected data.
	unique_flags = []
	add_nan = False
	for parameter in parameters:
		flag_column = parameter + ' QC Flag'
		unique_list = df[flag_column].unique()
		for flag in unique_list:
			flag = str(flag).split('.')[0]
			if flag == 'nan':
				add_nan = True
			elif flag not in unique_flags:
				unique_flags.append(flag)
	unique_flags.sort(key=int)
	if add_nan is True:
		unique_flags.append('nan')

	# Create a list of dictionaries where each dict shows the flag frequency for
	# one parameter.
	freq_list = []
	for parameter in parameters:
		# Count frequency of flags and store in a dictionary
		flag_column = parameter + ' QC Flag'
		flag_list = list(df[flag_column])
		freq_dict = {}
		for item in flag_list:
			item = str(item)
			if item in freq_dict:
				freq_dict[item] += 1
			else:
				freq_dict[item] = 1

		# Remove '.0' from flag names
		freq_dict_cleaned = {flag.split('.')[0] : freq
		 for flag, freq in freq_dict.items()}

		# Add 'missing' flags with 0 as value
		for flag in unique_flags:
			if flag not in freq_dict_cleaned.keys():
				freq_dict_cleaned[flag] = 0

		# Sort dictionary by the flags
		freq_dict_sorted = {flag : freq_dict_cleaned[flag]
		 for flag in sorted(freq_dict_cleaned.keys())}

		freq_list.append(freq_dict_sorted)

	# Transpose the freq_list into a dictionary with flag as keys and frequency
	# per parameter as value.
	# (This code only works when we have the same keys in each dict.)
	flag_dict = {k: [dic[k] for dic in freq_list] for k in freq_list[0]}

	#---------
	# MAKE FIGURE:
	# Position of the bars on the x-axis
	r = list(range(len(parameters)))

	# Store name of default color plotting list
	cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

	# Create 'bottom_list' indicating the height for plotting each flag.
	# (Flag1 is plotted at height 0, flag2 is plotted at height of flag 1,
	# flag 3 is plotted at height of flag1 + flag2, and so on...)
	previous_heights = [0] * len(parameters)
	bottom_list = [previous_heights]
	for value_list in flag_dict.values():
		next_heights = np.add(previous_heights, value_list).tolist()
		bottom_list.append(next_heights)
		previous_heights = next_heights

	# Get the figsize
	figsize = get_figsize(parameters)

	# Create figure
	f, ax = plt.subplots(figsize=figsize)

	# Add histogram bars to figure in a loop, one flag at the time
	legend_dict = {}
	for i in range(len(flag_dict)):
		bars = list(flag_dict.values())[i]
		bottom = bottom_list[i]
		ax = plt.bar(r, bars, bottom=bottom, color=cycle[i], width=barWidth)
		legend_dict[list(flag_dict.keys())[i]] = cycle[i]

	# Add legend
	patchList = []
	for key in legend_dict:
		data_key = mpatches.Patch(color=legend_dict[key], label=key)
		patchList.append(data_key)
	plt.legend(handles=patchList)

	# Add axis labels (depends on number of parameters/bars)
	if len(parameters) >= limit_nParameters:
		param_labels = [parameter.split(' [')[0] for parameter in parameters]
		plt.xticks(r, param_labels, rotation='vertical')
	else:
		param_labels = [parameter.split(' [')[0].replace(' ','\n')
					for parameter in parameters]
		plt.xticks(r, param_labels)

	plt.ylabel('Frequency')

	# Save file
	filename = 'stacked_bar_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename