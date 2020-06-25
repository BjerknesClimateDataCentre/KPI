###############################################################################
### BAR PLOT FOR OVERVIEW SECTION
###############################################################################

### Description of KPI:
# The kpi function 'overview_bar_plot' each create a figure with a histogram
# showing how the different parameters were flagged by the automatic QC.


#------------------------------------------------------------------------------
### Import packages

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import numpy as np
import os
import pandas as pd


#------------------------------------------------------------------------------
### Declare constants etc.

# Figure sizes
MAX_FIG_WIDTH = 9.5
MIN_FIG_WIDTH = 3
WIDTH_PER_PARAM = 1.5
FIG_HEIGHT = 4

# Width of bars
BAR_WIDTH = 0.75

# Number of parameters which change a-axis label to vertical to avoid overlap
LIMIT_N_PARAMS = 8

# Specify the color representing each QC flag (and missing value)
COLOR_DICT = {'2':'#85C0F9','3':'#A95AA1','4':'#F5793A', 'nan':'grey'}


#------------------------------------------------------------------------------
### Function

# Create a stacked barplot and store it in the output directory
def overview_bar_plot(meas_vocab, calc_vocab, df, output_dir):

	# Extract what is needed from meas_vocab and calc_vocab into param_dict
	parameter_dict = {
		config['col_header_name'] : config['fig_label_name_python']
		for config in meas_vocab.values()}

	parameter_dict.update(
		{config['col_header_name'] : config['fig_label_name_python']
		for config in calc_vocab.values()})

	#---------
	# STRUCTURE DATA FOR PLOTTING
	# Create a list of unique flags given to the parameters
	unique_flags = []
	add_nan = False
	for parameter in parameter_dict.keys():

		# Get all unique flags for this parameter
		unique = df[parameter + ' QC Flag'].unique()

		# Loop through the unique flags and add to the unique flags list
		for flag in unique:
			flag = str(flag).split('.')[0]	# Remove decimals
			if flag == 'nan':
				add_nan = True
			elif flag not in unique_flags:
				unique_flags.append(flag)

	# Sort the unique list and possibly add 'nan' to the end of list
	unique_flags.sort(key=int)
	if add_nan:
		unique_flags.append('nan')

	# Create a list of dictionaries where each dict shows the flag frequency
	# for one parameter
	freq_list = []
	for parameter in parameter_dict.keys():

		# Count frequency of flags and store in a dictionary
		flag_list = list(df[parameter + ' QC Flag'])
		freq_dict = {}
		# Loop through all flags and increase its count in the freq_dict (or
		# add to the freq_dict if does not already exist)
		for item in flag_list:
			item = str(item)
			if item in freq_dict:
				freq_dict[item] += 1
			else:
				freq_dict[item] = 1

		# Remove '.0' from flag names
		freq_dict_cleaned = {flag.split('.')[0] : freq
			for flag, freq in freq_dict.items()}

		# Add 'missing flags' as keys with 0 as value
		for flag in unique_flags:
			if flag not in freq_dict_cleaned.keys():
				freq_dict_cleaned[flag] = 0

		# Sort dictionary by the flags
		freq_dict_sorted = {flag : freq_dict_cleaned[flag]
			for flag in sorted(freq_dict_cleaned.keys())}

		freq_list.append(freq_dict_sorted)

	# Transpose the freq_list into a dictionary with flag as keys and frequency
	# per parameter as value. (This code only works when we have the same keys
	# in each dict.)
	flag_dict = {k: [dic[k] for dic in freq_list] for k in freq_list[0]}

	#---------
	# MAKE FIGURE:
	# Create list with positions of the bars on the x-axis
	x_position = list(range(len(parameter_dict)))

	# Create a color list based on the color dictionary
	color_list = []
	for flag in flag_dict.keys():
		color_list.append(COLOR_DICT[flag])

	# Create 'bottom_list' giving the height to plot each flag bar.
	# (Flag1 is plotted at height 0, flag2 is plotted at height of flag 1,
	# flag 3 is plotted at height of flag1 + flag2, and so on...)
	previous_heights = [0] * len(parameter_dict)
	bottom_list = [previous_heights]
	for value_list in flag_dict.values():
		next_heights = np.add(previous_heights, value_list).tolist()
		bottom_list.append(next_heights)
		previous_heights = next_heights

	# Define figure size (depends on number of parameters, but cannot
	# exceed min or max width)
	fig_width = sorted([MIN_FIG_WIDTH, WIDTH_PER_PARAM*len(parameter_dict),
		MAX_FIG_WIDTH])[1]
	figsize = (fig_width, FIG_HEIGHT)

	# Set up the figure
	f, ax = plt.subplots(figsize=figsize)

	# Add histogram bars to figure in a loop, one flag at the time
	legend_dict = {}
	for i in range(len(flag_dict)):
		bars = list(flag_dict.values())[i]
		bottom = bottom_list[i]
		ax = plt.bar(x_position, bars, bottom=bottom, color=color_list[i],
			width=BAR_WIDTH)
		legend_dict[list(flag_dict.keys())[i]] = color_list[i]

	# Add legend
	patch_list = []
	for key in legend_dict:
		data_key = mpatches.Patch(color=legend_dict[key], label=key)
		patch_list.append(data_key)
	plt.legend(handles=patch_list)

	# Add axis labels (depends on number of parameters/bars)
	if len(parameter_dict) >= LIMIT_N_PARAMS:
		param_labels = [label.split(' [')[0]
					for parameter, label in parameter_dict.items()]
		plt.xticks(x_position, param_labels, rotation='vertical')
	else:
		param_labels = [label.split(' [')[0].replace(' ','\n')
					for parameter, label in parameter_dict.items()]
		plt.xticks(x_position, param_labels)

	plt.ylabel('Frequency')

	# Save figure to file and close figure
	filename = 'overview_bar_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()