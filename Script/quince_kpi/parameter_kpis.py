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
#  - move word 'outliers' since this is defined as something that might
# be different from waht we mean. ' We use the method to scale the plot'.


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os
import numpy as np


#------------------------------------------------------------------------------
### Set variables

# Figure sizes
pie_fig_size = 2.5
line_fig_width = 9
line_fig_height = 4.5

# Plot symbol alpha
alpha = 0.7

# QC Flag color dictionary
color_dict = {'2':'green','3':'orange','4':'red', 'nan':'grey'}

# Title fontsize:
title_fontsize = 9

# Factor used to define upper and lower plot range
k = 1.5


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


def make_plot(df, parameter, ax):
	# Identify the parameters QC flag columns
	color_column = parameter + ' QC Flag'

	# Remove NaNs from color_dict since missing values are not plotted
	color_dict_noNan = color_dict
	if 'nan' in color_dict:
		color_dict_noNan.pop('nan')

	for flag, col in color_dict_noNan.items():
		limited_df = df[df[color_column]==int(flag)]
		ax.scatter(x=limited_df['Date/Time'], y=limited_df[parameter],
					c=col, label=flag, alpha=alpha, edgecolors='none',
					marker='.')

def single_line_plot(parameter, short_name, df, output_dir, **kwargs):

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
	cut_off = iqr * k
	lower = q25 - cut_off
	upper = q75 + cut_off

	# Set up the figure
	fig, ax = plt.subplots(figsize=(line_fig_width,line_fig_height))

	# Create the first plot with all values (colored by QC flag)
	ax = plt.subplot2grid((2, 1), (0,0))
	make_plot(df=df, parameter=parameter, ax=ax)

	# Add the lower and upper values to plot
	plt.axhline(y=upper, color='blue', linestyle='-')
	plt.axhline(y=lower, color='blue', linestyle='-')

	# Add grid and labels etc.
	ax.grid(True)
	fig.autofmt_xdate()
	plt.ylabel(parameter)
	ax.set_title('a)', loc='left', fontsize=title_fontsize, fontweight='bold')

	# Create the second plot removing values outside upper and lower range
	ax = plt.subplot2grid((2, 1), (1,0))
	df_scaled = df[(df[parameter] > lower) & (df[parameter] < upper)]
	make_plot(df=df_scaled, parameter=parameter, ax=ax)

	# Add grid, labels etc.
	ax.legend()
	ax.grid(True)
	fig.autofmt_xdate()
	plt.ylabel(parameter)
	ax.set_title('b)', loc='left', fontsize=title_fontsize, fontweight='bold')
	#plt.xlabel('Time')

	# Save the plot to file
	filename = short_name + '_single_line_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename