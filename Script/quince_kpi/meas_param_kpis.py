###############################################################################
### KPI plots/tables for individual measured parameters
###############################################################################

### Description:
# - KPI function for creating a pie chart for a single parameter
# - KPI function for creating two line plots for a single paramter. One plot
# showing all measurements, the other scaled (only k times IQR)
#
# TODO:
#  - in single_line_plot:
#     - make one common y label
#  - move word 'outliers' since this is defined as something that might
# be different from waht we mean. ' We use the method to scale the plot'.


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os
import numpy as np


#------------------------------------------------------------------------------
### Declair constants etc.

# Figure sizes
PIE_FIG_SIZE = 2.5
LINE_FIG_WIDTH = 9
LINE_FIG_HEIGHT = 4.5

# Plot symbol alpha (related to transparency)
ALPHA = 1

# QC Flag color dictionary
COLOR_DICT = {'2':'#85C0F9','3':'#A95AA1','4':'#F5793A', 'nan':'grey'}
CONTRAST_COLOR = '#0F2080'

# Title fontsize:
TITLE_FONTSIZE = 9

# Factor used to define upper and lower plot range
K = 1.5


#------------------------------------------------------------------------------
### Functions

def meas_param_flag_piechart(parameter, meas_param_config, df,
	output_dir):

	# Store the parameters QC flags in a list (remove '.0' if needed)
	flag_list = list(df[parameter + ' QC Flag'])
	flag_list_cleaned = [str(item).split('.')[0] for item in flag_list]

	# Get the unique flags and their frequencies (as arrays)
	unique_flags, freq = np.unique(flag_list_cleaned, return_counts=True)

	# Create color list:
	color_list = []
	for flag in list(unique_flags):
		if flag == 'nan':
			color_list.append('grey')
		else:
			color_list.append(COLOR_DICT[flag])
	# Create pie chart
	plt.subplots(figsize=(PIE_FIG_SIZE,PIE_FIG_SIZE))
	patches, text, autotexts = plt.pie(freq, colors=color_list, startangle=90,
		autopct='%1.0f%%')
	for autotext in autotexts:
		autotext.set_color('white')
	plt.legend(patches, list(unique_flags), loc="best")
	plt.axis('equal')
	plt.tight_layout()

	# Save the plot to file and close figure
	filename = meas_param_config[parameter]['short_name'] + '_meas_param_flag_piechart.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()


def make_plot(df, parameter, ax):
	# Identify the parameters QC flag columns
	color_column = parameter + ' QC Flag'

	# Remove NaNs from color_dict since missing values are not plotted
	color_dict_noNan = COLOR_DICT
	if 'nan' in COLOR_DICT:
		color_dict_noNan.pop('nan')

	for flag, col in color_dict_noNan.items():
		limited_df = df[df[color_column]==int(flag)]
		ax.scatter(x=limited_df['Date/Time'], y=limited_df[parameter],
					c=col, label=flag, alpha=ALPHA, edgecolors='none',
					marker='.')


def meas_param_line_plot(parameter, meas_param_config, df, output_dir):

	# Remove rows with NaNs
	df = df.dropna(subset=[parameter])

	# The figure created will contain two plots: a) show all measurements, b)
	# show measurements where the highest and lowest values are removed
	# (scaled). Use the following method to define the upper and lower cutoffs:
	# "The IQR can be used to identify outlier by defining limits on the sample
	# values that are a factor k of the IQR below the 25th percentile or
	# above the 75th percentile. The common value for the factor k is the value
	# 1.5. A factor k of 3 or more can be used to identify values that are
	# extreme outliers or “far outs” when described in the context of box and
	# whisker plots (https://machinelearningmastery.com/how-to-use-statistics-to-identify-outliers-in-data/)

	# Calculate the IQR, cutoffs, and the lower and upper ranges
	q25 = np.percentile(df.loc[:,parameter], 25)
	q75 = np.percentile(df.loc[:,parameter], 75)
	iqr = q75 - q25
	cut_off = iqr * K
	lower = q25 - cut_off
	upper = q75 + cut_off

	# Set up the figure
	fig, ax = plt.subplots(figsize=(LINE_FIG_WIDTH,LINE_FIG_HEIGHT))

	# Create the first plot with all values (colored by QC flag)
	ax = plt.subplot2grid((2, 1), (0,0))
	make_plot(df=df, parameter=parameter, ax=ax)

	# Add the lower and upper values to plot
	plt.axhline(y=upper, color=CONTRAST_COLOR, linestyle='-')
	plt.axhline(y=lower, color=CONTRAST_COLOR, linestyle='-')

	# Add grid and labels etc.
	ax.grid(True)
	fig.autofmt_xdate()
	plt.ylabel(meas_param_config[parameter]['fig_label_name_python'])
	ax.set_title('a)', loc='left', fontsize=TITLE_FONTSIZE, fontweight='bold')

	# Create the second plot removing values outside upper and lower range
	ax = plt.subplot2grid((2, 1), (1,0))
	df_scaled = df[(df[parameter] > lower) & (df[parameter] < upper)]
	make_plot(df=df_scaled, parameter=parameter, ax=ax)

	# Add grid, labels etc.
	ax.legend()
	ax.grid(True)
	fig.autofmt_xdate()
	#plt.ylabel(meas_param_config[parameter]['fig_label_name_python'])
	ax.set_title('b)', loc='left', fontsize=TITLE_FONTSIZE, fontweight='bold')
	#plt.xlabel('Time')

	# Save the plot to file and close figure
	filename = meas_param_config[parameter]['short_name'] + '_meas_param_line_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()


def meas_qc_comment_table(parameter, meas_param_config, df):

	# Store the parameters QC comments in a list and remove nan's.
	comment_list = list(df[parameter + ' QC Comment'])
	comment_list = [x for x in comment_list if x == x]

	# Split comments if they contain ';' (means more than one comment in a row)
	comment_list_cleaned = []
	for comment in comment_list:
		if ';' in comment:
			splitted = comment.split('; ')
			comment_list_cleaned.extend(splitted)
		else:
			comment_list_cleaned.append(comment)

	# Extract unique comments and their frequency and store in a dictonary
	unique_comments, freq = np.unique(comment_list_cleaned, return_counts=True)
	tabel_dict = dict(zip(list(unique_comments), list(freq)))

	# Sort dictionary by the frequency, high to low.
	tabel_dict_sorted = {k: v for k, v in sorted(tabel_dict.items(),
		key=lambda item: item[1], reverse=True)}

	# Add header and percentages to each frequency
	tabel_dict_percent = {'QC Comment': 'Frequencies'}
	for key, value in tabel_dict_sorted.items():
		percent = round((value/df.shape[0])*100,2)
		tabel_dict_percent[key] = str(value) + ' (' + str(percent) + '%)'

	return tabel_dict_percent