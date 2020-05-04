###############################################################################
### KPI plots/tables for individual parameters
###############################################################################

### Description:
# - Function for creating a pie chart for a single parameter
# - Function for creating two line plots for a single paramter. One plot showing
# all measurements, the other witout outliers (defined as ...)

# TODO:
#  - in single_line_plot:
#     - make one common y label


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os
import numpy as np


#------------------------------------------------------------------------------
### Set variables

# Figure sizes
pie_fig_size = 4
line_fig_width = 9.5
line_fig_height = 6

# Plot symbol alpha
alpha = 0.7

# QC Flag color dictionary
color_dict = {'2':'green','3':'orange','4':'red', 'nan':'grey'}

# Title fontsize:
title_fontsize = 14


#------------------------------------------------------------------------------
### Functions

def flag_piechart(parameter, short_name, df, output_dir, **kwargs):

	# Store the parameters QC flags in a list (remove '.0' if needed)
	flag_list = list(df[parameter + ' QC Flag'])
	flag_list_cleaned = [str(item).split('.')[0] for item in flag_list]

	# Get the unique flags and their frequencies
	flag_freq = np.unique(flag_list_cleaned, return_counts=True)
	unique_flags = flag_freq[0]
	freq = flag_freq[1]

	# Create color list:
	color_list = []
	for flag in unique_flags:
		color_list.append(color_dict[flag])

	# Create pie chart
	plt.subplots(figsize=(pie_fig_size,pie_fig_size))
	patches, texts = plt.pie(freq, colors=color_list, startangle=90)
	plt.legend(patches, unique_flags, loc="best")
	plt.axis('equal')
	plt.tight_layout()

	# Save the plot to file
	filename = short_name + '_flag_piechart.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename


def single_line_plot(parameter, short_name, df, output_dir, **kwargs):

	# Remove rows with NaNs
	df = df.dropna(subset=[parameter])
	#df = df[df[parameter] > 0]


	# Identify the parameters QC flag columns
	color_column = parameter + ' QC Flag'

	# Remove NaNs from color_dict since we cannot see the missing values
	color_dict_noNan = color_dict
	color_dict_noNan.pop('nan')

	# The figure created will contain two plots: a) show all measurements, b)
	# show measurements without outliers.
	# "The IQR can be used to identify outlier by defining limits on the
	# sample values that are a factor k of the IQR below the 25th percentile or
	# above the 75th percentile. The common value for the factor k is the value
	# 1.5. A factor k of 3 or more can be used to identify values that are
	# extreme outliers or “far outs” when described in the context of box and
	# whisker plots (https://machinelearningmastery.com/how-to-use-statistics-to-identify-outliers-in-data/)
	# Plot b) show measurements within k=1.5 as cutoff. Plot a) will, in
	# addition to all values, show the lower and upper outlier cut offs as
	# lines, both with k=1.5 and k=3. In this way the reader can decide for
	# themselves if the 1.5 cutoff is sufficient in each case.

	# Calculate the IQR, the outlier cutoffs, and the lower and upper ranges
	q25 = np.percentile(df.loc[:,parameter], 25)
	q75 = np.percentile(df.loc[:,parameter], 75)
	iqr = q75 - q25
	cut_off = iqr * 1.5
	cut_off_extreme = iqr * 3
	lower = min(q25 - cut_off,0)
	upper = q75 + cut_off
	lower_extreme = min(q25 - cut_off_extreme, 0)
	upper_extreme = q75 + cut_off_extreme

	# Set up the figure
	fig, ax = plt.subplots(figsize=(line_fig_width,line_fig_height))

	# Create the first plot with all values (colored by flag)
	ax = plt.subplot2grid((2, 1), (0,0))

	# Add one flag at the time to the plot
	for flag, col in color_dict_noNan.items():
		limited_df = df[df[color_column]==int(flag)]
		ax.scatter(x=limited_df['Date/Time'], y=limited_df[parameter],
					c=col, label=flag, alpha=alpha, edgecolors='none',
					marker='.')

	# Add the lower and upper values to plot a), and text with the k value
	plt.axhline(y=upper, color='blue', linestyle='-')
	plt.axhline(y=upper_extreme, color='blue', linestyle='-')
	ax.text(max(df['Date/Time']), upper, 'k = 1.5', color='blue', fontsize=13,
		style='italic', fontweight='bold', backgroundcolor='w')
	ax.text(max(df['Date/Time']), upper_extreme, 'k = 3.0', color='blue',
		fontsize=13, style='italic', fontweight='bold', backgroundcolor='w')

	# Add grid and labels etc.
	ax.grid(True)
	fig.autofmt_xdate()
	plt.ylabel(parameter)
	ax.set_title('a)', loc='left', fontsize=title_fontsize, fontweight='bold')

	# Create the second plot removing outliers
	ax = plt.subplot2grid((2, 1), (1,0))

	# Create new data frame whene outliers are excluded
	df_outliers_removed = df[(df[parameter] > lower) & (df[parameter] < upper)]

	# Add one flag at the time to the plot
	for flag, col in color_dict_noNan.items():
		limited_df = df_outliers_removed[df_outliers_removed[color_column]==int(flag)]
		ax.scatter(x=limited_df['Date/Time'],
				y=limited_df[parameter], c=col, label=flag,
				alpha=alpha, edgecolors='none', marker='.')

	# Add grid, labels etc.
	ax.legend()
	ax.grid(True)
	fig.autofmt_xdate()
	plt.ylabel(parameter)
	ax.set_title('b)', loc='left', fontsize=title_fontsize, fontweight='bold')

	#plt.xlabel('Time')

	# Save the plot to file
	filename = short_name + '_lineplot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename