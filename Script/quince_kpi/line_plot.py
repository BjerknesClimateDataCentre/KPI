###############################################################################
### FIGURE VISUALISING THE DATA VALUES FOR ONE PARAMETER
###############################################################################

### Description of the KPI functions:
# - 'line_plot' creates a figure with two subplots, one showing all
# measurements from one parameter, the other plot scaled to improve visibility
# in cases of very high/low values. We use the following method to define the
# upper and lower cutoffs for this scaling: "The IQR can be used to identify
# outlier by defining limits on the sample values that are a factor k of the
# IQR below the 25th percentile or above the 75th percentile. The common value
# for the factor k is the value 1.5." (https://machinelearningmastery.com
# /how-to-use-statistics-to-identify-outliers-in-data/).


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
COLOR_DICT = {'2':'#85C0F9','3':'#A95AA1','4':'#F5793A'}
CONTRAST_COLOR = '#0F2080'

# Title fontsize:
TITLE_FONTSIZE = 9

# Factor to multiply with IQR's to define upper and lower y-range in line plot
K = 1.5


#------------------------------------------------------------------------------
### Functions

# Create a subplot in loop - one flag at the time. Add grid and title.
def create_subplot(df, header, ax, letter):
	for flag, col in COLOR_DICT.items():
		df_edit = df[df[header + ' QC Flag']==int(flag)]
		ax.scatter(x=df_edit['Date/Time'], y=df_edit[header], c=col,
			label=flag, alpha=ALPHA, edgecolors='none', marker='.')
	ax.grid(True)
	ax.set_title(letter, loc='left', fontsize=TITLE_FONTSIZE,
		fontweight='bold')

# Create figure with two subplots for a parameter, one showing all
# measurements/values, the other scaled to improve visibility
def line_plot(parameter, vocab, df, output_dir):

	# Remove rows in data frame with missing values
	header = vocab[parameter]['col_header_name']
	df = df.dropna(subset=[header])

	# Calculate upper and lower cut-offs (method described at top of this file)
	q25 = np.percentile(df.loc[:,header], 25)
	q75 = np.percentile(df.loc[:,header], 75)
	cut_off = (q75 - q25) * K
	lower, upper = q25 - cut_off, q75 + cut_off

	# Set up the figure
	fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True,
		figsize=(LINE_FIG_WIDTH,LINE_FIG_HEIGHT))

	# Create first subplot with all values, add cut-off lines, and legend
	create_subplot(df=df, header=header, ax=axs[0], letter='a)')
	axs[0].axhline(y=upper, color=CONTRAST_COLOR, linestyle='-')
	axs[0].axhline(y=lower, color=CONTRAST_COLOR, linestyle='-')
	axs[0].legend()

	# Create second subplot excluding values outside upper and lower cut-offs
	df_scaled = df[(df[header] > lower) & (df[header] < upper)]
	create_subplot(df=df_scaled, header=header, ax=axs[1], letter='b)')

	# Add y and x labels
	fig.text(0.05, 0.5, vocab[parameter]['fig_label_name_python'],
		verticalalignment='center', rotation='vertical')
	fig.autofmt_xdate()

	# Save the plot to file and close figure
	filename = parameter + '_line_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()