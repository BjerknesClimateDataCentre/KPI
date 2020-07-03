###############################################################################
### FIGURE VISUALISING THE DATA VALUES
###############################################################################

### Description of the KPI functions:
# - 'meas_line_plot' creates a figure with two subplots, one showing all
# measurements from one parameter (sensor), the other plot scaled to improve
# visibility in cases of very high/low valus. We use the following method to
# define the upper and lower cutoffs for this scaling: "The IQR can be used to
# identify outlier by defining limits on the sample values that are a factor k
# of the IQR below the 25th percentile or above the 75th percentile. The common
# value for the factor k is the value 1.5." (https://machinelearningmastery.
# com/how-to-use-statistics-to-identify-outliers-in-data/).


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os
import numpy as np


#------------------------------------------------------------------------------
### Declare constants etc.

# Figure sizes
LINE_FIG_WIDTH = 9
LINE_FIG_HEIGHT = 4.5

# Plot symbol alpha (related to transparency)
ALPHA = 1

# Specify the color representing each QC flag (and missing value)
COLOR_DICT = {'2':'#85C0F9','3':'#A95AA1','4':'#F5793A', 'nan':'grey'}
CONTRAST_COLOR = '#0F2080'

# Title fontsize:
TITLE_FONTSIZE = 9

# Factor to multiply with IQR's to define upper and lower y-range in line plot
K = 1.5


#------------------------------------------------------------------------------
### Functions

# Make a subplot for the meas_line_plot figure
def make_plot(df, col_header_name, ax):

	# Remove NaNs from color_dict since missing values are not plotted
	color_dict_noNan = COLOR_DICT
	if 'nan' in COLOR_DICT:
		color_dict_noNan.pop('nan')

	# Create subplot in loop - one flag at the time
	for flag, col in color_dict_noNan.items():
		df_edit = df[df[col_header_name + ' QC Flag']==int(flag)]
		ax.scatter(x=df_edit['Date/Time'], y=df_edit[col_header_name],
					c=col, label=flag, alpha=ALPHA, edgecolors='none',
					marker='.')

# Creates figure with two subplots for a parameter (sensor), one with all
# measurements, the other scaled
def line_plot(parameter, vocab, df, output_dir, var_config):

	# Remove rows where parameter value is missing
	col_header_name = vocab[parameter]['col_header_name']
	df = df.dropna(subset=[col_header_name])

	# Calculate the IQR, cutoffs, and the lower and upper ranges
	q25 = np.percentile(df.loc[:,col_header_name], 25)
	q75 = np.percentile(df.loc[:,col_header_name], 75)
	iqr = q75 - q25
	cut_off = iqr * K
	lower = q25 - cut_off
	upper = q75 + cut_off

	# Set up the figure
	fig, ax = plt.subplots(figsize=(LINE_FIG_WIDTH,LINE_FIG_HEIGHT))

	# Create the first subplot with all values (colored by QC flag)
	ax = plt.subplot2grid((2, 1), (0,0))
	make_plot(df=df, col_header_name=col_header_name, ax=ax)

	# Add the lower and upper cut-off lines to subplotplot
	plt.axhline(y=upper, color=CONTRAST_COLOR, linestyle='-')
	plt.axhline(y=lower, color=CONTRAST_COLOR, linestyle='-')

	# Add grid, axis labels and letter
	ax.grid(True)
	plt.ylabel(vocab[parameter]['fig_label_name_python'])
	ax.set_title('a)', loc='left', fontsize=TITLE_FONTSIZE, fontweight='bold')

	# Create the second plot removing values outside upper and lower range
	ax = plt.subplot2grid((2, 1), (1,0))
	df_scaled = df[(df[col_header_name] > lower)
		& (df[col_header_name] < upper)]
	make_plot(df=df_scaled, col_header_name=col_header_name, ax=ax)

	# Add grid, labels and letter
	ax.legend()
	ax.grid(True)
	fig.autofmt_xdate()
	ax.set_title('b)', loc='left', fontsize=TITLE_FONTSIZE, fontweight='bold')

	# Save the plot to file and close figure
	filename = parameter + '_line_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()