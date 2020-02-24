###############################################################################
###                                                                         ###
###############################################################################

### Description:
#

#------------------------------------------------------------------------------
#import pandas as pd
import matplotlib.pyplot as plt
import os
import string
import math


def make_subplot(colname, df, cleaned, ax):

	# Remove rows with NaNs
	df = df.dropna(subset=[colname])

	# Identify the parameters QC flag columns
	color_column = colname + ' QC Flag'

	# If cleaned is false, plot all data. Else, plot data with QC flag 2.
	if cleaned is False:
		# Set plot color for the QC flags and plot one flag at the time
		color_code = {2:'green',3:'orange',4:'red'}
		for flag, col in color_code.items():
				limited_df = df[df[color_column]==flag]
				ax.scatter(x=limited_df['Date/Time'], y=limited_df[colname],
					c=col, label=flag, alpha=0.7, edgecolors='none', marker='.')

# HOW TO ADD LEGENG WITH FLAG CODES
				#ax.legend(fontsize=9, bbox_to_anchor=(1, 1))
		#if letter_count == 0:
			#ax.legend(fontsize=9, bbox_to_anchor=(1, 1))
		#if row_count == 0 and col_count == 1:
			#ax.legend(fontsize=9, bbox_to_anchor=(1, 1))

		else:
			limited_df = df[df[color_column]==2]
			ax.scatter(x=limited_df['Date/Time'], y=limited_df[colname],
				c='green', alpha=0.7, edgecolors='none', marker='.')

	ax.grid(True)


# Function plots parameter(s) vs time and saves plot(s) in output directory
def plot_data(colnames, df, output_dir, cleaned=False):

	# Decide limit when plot in two columns:
	plot_limit = 4

	# Get number of columns to plot
	n_plot=len(colnames)

	# Set figsize
	fig_width = 9.5
	plot_height = 3
	if n_plot <= plot_limit:
		fig_height = plot_height*n_plot
	else:
		fig_height = plot_height*n_plot/2
	figsize = (fig_width, fig_height)

	# List of letters used for labelling the plots
	letters=list(string.ascii_lowercase[0:n_plot])

	# Set up the plot
	fig, ax = plt.subplots(sharex=True, figsize=figsize)

	letter_count = 0
	row_count = 0
	col_count = 0
	for colname in colnames:

		# Specify where in the figure to plot the next parameter
		if n_plot > 1 and n_plot <= 4:
			ax = plt.subplot2grid((n_plot, 1), (letter_count,0))
		elif n_plot > 5 and n_plot <= 8:
			ax = plt.subplot2grid((math.ceil(n_plot/2), 2), (row_count,col_count))
		else:
			ax = plt.subplot2grid((math.ceil(n_plot/3), 3), (row_count,col_count))

		# Make subplot
		make_subplot(colname, df, cleaned, ax)

		# Add title (and letter if needed)
		if n_plot == 1:
			plt.title('     ' + colnames[0], fontsize=10, fontweight='bold')
		else:
			title = letters[letter_count] + ')     ' + colname
			ax.set_title(title, loc='left', fontsize=10,
				fontweight='bold')

		# !!! Increase counters in a better way !!!
		# Increase counters
		letter_count += 1

		if n_plot > 5 and n_plot <= 8:
			if col_count == 1:
				col_count = 0
				row_count += 1
			else:
				col_count = 1
		else:
			if letter_count %3 == 0:
				row_count += 1
			if col_count == 0:
				col_count = 1
			elif col_count == 1:
				col_count = 2
			elif col_count == 2:
				col_count = 0

	#----------------------
	# Add x-axis sideways
	fig.autofmt_xdate()

	# Save plot to file
	if cleaned is True:
		filename = 'kpi_plot_data_cleaned.png'
	else:
		filename = 'kpi_plot_data.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename