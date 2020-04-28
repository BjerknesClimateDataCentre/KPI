###############################################################################
### KPI: Line plot(s)                                                       ###
###############################################################################

### Description:
# This KPI provides a visualisation of the data.

#----------
# TODO:
# - Style these plots as if they were default seaborn plots (use sns.set())
# - Improve layout when plot in three columns (things collide)
# - Time label is not added if there is no subplot in the lowest row (e.g. when
# plot 5 params). Fix this!


#------------------------------------------------------------------------------
### Import packages

import matplotlib.pyplot as plt
import os
import string
import math


#------------------------------------------------------------------------------
### Set variables

# Maximum number of plots to allow with 1 column and 2 columns
limit_1col = 3
limit_2col = 8

# Figure sizes
fig_width = 9.5
fig_height = 3

# Plot symbol alpha
alpha = 0.7

# Title fontsize:
title_fontsize = 8

#------------------------------------------------------------------------------
### Functions

# Returns how many rows and columns of subplots in the resulting figure
def get_row_col(n_plot):
	if n_plot <= limit_1col:
		n_col = 1
	elif n_plot > limit_1col and n_plot <= limit_2col:
		n_col = 2
	else:
		n_col = 3
	n_row = math.ceil(n_plot/n_col)

	return n_row, n_col


def make_subplot(parameter, df, cleaned, ax):
	# Remove rows with NaNs
	df = df.dropna(subset=[parameter])

	# Identify the parameters QC flag columns
	color_column = parameter + ' QC Flag'

	# If cleaned is false, plot all data. Else, plot data with QC flag 2.
	if cleaned is False:
		# Set plot color for the QC flags and plot one flag at the time
		color_code = {2:'green',3:'orange',4:'red'}
		for flag, col in color_code.items():
				limited_df = df[df[color_column]==flag]
				ax.scatter(x=limited_df['Date/Time'], y=limited_df[parameter],
					c=col, label=flag, alpha=alpha, edgecolors='none',
					marker='.')
	else:
		limited_df = df[df[color_column]==2]
		ax.scatter(x=limited_df['Date/Time'], y=limited_df[parameter],
			c='green', alpha=alpha, edgecolors='none', marker='.')

	ax.grid(True)
	# !!! To adjust the suplots- Try this:
	#plt.subplots_adjust(bottom=0.2, wspace=0.35)
	# Other inputs are: top, left, right, hspace


# Function plots parameter(s) vs time, saves the figure in the output
# directory, and returns the figures filename back to the main script.
def line_plot(parameters, df, output_dir, **kwargs):

	# Create variables from kwargs
	# !!! Must be a different way to use kwargs to that this step is not needed
	cleaned = kwargs['kwargs']['cleaned']

	# Store number of plots to create
	n_plot = len(parameters)

	# Get the number of rows and columns in figure
	n_row, n_col = get_row_col(n_plot)

	# Set up the plot
	figsize = (fig_width, fig_height*n_row)
	fig, ax = plt.subplots(sharex=True, figsize=figsize)

	# Loop through all row and column positions and make their subplots
	count = 0
	for row in range(n_row):
		for col in range(n_col):

			# Specify which param to plot, and where.
			parameter = parameters[count]
			ax = plt.subplot2grid((n_row, n_col), (row,col))

			# Make subplot
			make_subplot(parameter, df, cleaned, ax)
			ax.legend()
			# !!! HOW TO ADD ONLY ONCE??
			#ax.legend(fontsize=9, bbox_to_anchor=(1, 1)) ???

			# Add title (and letter if needed)
			if n_plot == 1:
				plt.title('     ' + parameters[0], fontsize=title_fontsize,
					fontweight='bold')
			else:
				title = string.ascii_lowercase[count] + ')     ' + parameter
				ax.set_title(title, loc='left', fontsize=title_fontsize,
					fontweight='bold')

			# Increase counter (stop when exceeds number of params)
			count += 1
			if count >= n_plot:
				break

	# Add x-axis sideways
	fig.autofmt_xdate()

	# Save plot to file
	if cleaned is True:
		filename = 'line_plot.png'
	else:
		filename = 'line_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename