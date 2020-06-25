###############################################################################
### LINE PLOT FOR OVERVIEW SECTION
###############################################################################

### Description of KPI:
# The kpi function 'overview_line_plot' creates a figure which visualises all
# parameters (measured or calculated) evaluated in the report. The figure
# contains one subplot per parameter. The subplots are arranged in one or two
# columns depending on the number of parameters. The dot colors indicate the
# QC flag assigned.


#------------------------------------------------------------------------------
### Import packages

import matplotlib.pyplot as plt
import os
import string
import math


#------------------------------------------------------------------------------
### Declare constants etc.

# Layout adjustments related to the number of parameters/subplots
LIMIT_1COL = 3
LIMIT_HEIGHT_2 = 8
LIMIT_HEIGHT_3 = 12

# Figure sizes
FIG_WIDTH = 9.5
PLOT_HEIGHT_1 = 3
PLOT_HEIGHT_2 = 2.5
PLOT_HEIGHT_3 = 2

# Plot symbol alpha (related to transparency)
ALPHA = 0.7

# Title fontsize:
TITLE_FONTSIZE = 9

# Specify the color representing each QC flag
COLOR_DICT = {'2':'#85C0F9','3':'#A95AA1','4':'#F5793A'}


#------------------------------------------------------------------------------
### Function

# Create line plot figure and store it in the output directory
def overview_line_plot(meas_vocab, calc_vocab, df, output_dir):

	# Extract what is needed from meas_vocab and calc_vocab into param_dict
	parameter_dict = {
		config['col_header_name'] : config['fig_label_name_python']
		for config in meas_vocab.values()}

	parameter_dict.update(
		{config['col_header_name'] : config['fig_label_name_python']
		for config in calc_vocab.values()})


	# Get number of subplots
	n_plot = len(parameter_dict)

	# Set number of rows and columns for the subplots
	if n_plot <= LIMIT_1COL:
		n_col = 1
	else:
		n_col = 2
	n_row = math.ceil(n_plot/n_col)

    # Set height of each subplot
	if n_plot > LIMIT_HEIGHT_3:
		plot_height = PLOT_HEIGHT_3
	elif n_plot > LIMIT_HEIGHT_2:
		plot_height = PLOT_HEIGHT_2
	else:
		plot_height = PLOT_HEIGHT_1

	# Set up the figure
	fig, ax = plt.subplots(sharex=True, figsize=(FIG_WIDTH, plot_height*n_row))

	# Loop through all row and column positions and create each subplot
	subplot_count = 0
	for row in range(n_row):
		for col in range(n_col):

			# Specify which parameter to plot
			parameter = list(parameter_dict.keys())[subplot_count]

			# Create copy of df witouh missing values for the current parameter
			df_edit = df.dropna(subset=[parameter])

			# Specify subplot location
			ax = plt.subplot2grid((n_row, n_col), (row, col))

			# Create subplot in loop - one flag at the time
			for flag, col in COLOR_DICT.items():
				df_edit2 = df_edit[df_edit[parameter + ' QC Flag']==int(flag)]
				ax.scatter(x=df_edit2['Date/Time'], y=df_edit2[parameter],
					c=col, label=int(flag), alpha=ALPHA, edgecolors='none',
					marker='.')

			# Add subplot grid, legend and tittle
			ax.grid(True)

			if subplot_count == 0:
				ax.legend()

			title = '{letter})     {param_label}'.format(
				letter=string.ascii_lowercase[subplot_count],
				param_label=list(parameter_dict.values())[subplot_count])
			ax.set_title(title, loc='left', fontsize=TITLE_FONTSIZE,
				fontweight='bold')

			# Increase subplot_count (stop when reach total number of subplots)
			subplot_count += 1
			if subplot_count == n_plot:
				break

	# Add shared x-axis sideways to bottom subplots
	fig.autofmt_xdate()

	# Save figure to file and close figure
	filename = 'overview_line_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()