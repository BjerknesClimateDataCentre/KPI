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
### Declair constants etc.

# Layout adjustments related to the number of plots in figure
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

# QC Flag color dictionary
COLOR_DICT = {'2':'#85C0F9','3':'#A95AA1','4':'#F5793A'}


#------------------------------------------------------------------------------
### Functions

# Returns how many rows and columns of subplots in the resulting figure
def get_row_col(n_plot):
	if n_plot <= LIMIT_1COL:
		n_col = 1
	elif n_plot > LIMIT_1COL:
		n_col = 2
	n_row = math.ceil(n_plot/n_col)

	return n_row, n_col


def make_subplot(parameter, df, cleaned, ax):
	# Remove rows with NaNs
	df = df.dropna(subset=[parameter])

	# Identify the parameters QC flag columns
	flag_column = parameter + ' QC Flag'

	# If cleaned is false, plot all data. Else, plot data with QC flag 2.
	if cleaned is False:
		# Set plot color for the QC flags and plot one flag at the time
		for flag, col in COLOR_DICT.items():
				limited_df = df[df[flag_column]==int(flag)]
				ax.scatter(x=limited_df['Date/Time'], y=limited_df[parameter],
					c=col, label=int(flag), alpha=ALPHA, edgecolors='none',
					marker='.')
	else:
		limited_df = df[df[flag_column]==2]
		ax.scatter(x=limited_df['Date/Time'], y=limited_df[parameter],
			c='green', alpha=ALPHA, edgecolors='none', marker='.')

	ax.grid(True)
	# !!! To adjust the suplots- Try this:
	#plt.subplots_adjust(bottom=0.2, wspace=0.35)
	# Other inputs are: top, left, right, hspace


# Function plots parameter(s) vs time, saves the figure in the output
# directory, and returns the figures filename back to the main script.
def intro_line_plot(parameter_dict, df, output_dir, **kwargs):

	# Create variables from kwargs
	# !!! Must be a different way to use kwargs to that this step is not needed
	cleaned = kwargs['kwargs']['cleaned']

	# Store number of plots to create
	n_plot = len(parameter_dict)

	# Get the number of rows and columns in figure
	n_row, n_col = get_row_col(n_plot)

	# Set up the figure
	if n_plot > LIMIT_HEIGHT_3:
		plot_height = PLOT_HEIGHT_3
	elif n_plot > LIMIT_HEIGHT_2:
		plot_height = PLOT_HEIGHT_2
	else:
		plot_height = PLOT_HEIGHT_1

	figsize = (FIG_WIDTH, plot_height*n_row)
	fig, ax = plt.subplots(sharex=True, figsize=figsize)

	# Loop through all row and column positions and make their subplots
	count = 0
	for row in range(n_row):
		for col in range(n_col):

			# Specify which param to plot, and where.
			parameter = list(parameter_dict.keys())[count]
			ax = plt.subplot2grid((n_row, n_col), (row,col))

			# Make subplot
			make_subplot(parameter, df, cleaned, ax)
			ax.legend()
			# !!! HOW TO ADD ONLY ONCE??
			#ax.legend(fontsize=9, bbox_to_anchor=(1, 1)) ???

			# Add title (and letter if needed)
			if n_plot == 1:
				plt.title('     ' + list(parameter_dict.values())[count], fontsize=TITLE_FONTSIZE,
					fontweight='bold')
			else:
				title = string.ascii_lowercase[count] + ')     ' + list(parameter_dict.values())[count]
				ax.set_title(title, loc='left', fontsize=TITLE_FONTSIZE,
					fontweight='bold')

			# Increase counter (stop when exceeds number of params)
			count += 1
			if count >= n_plot:
				break

	# If odd number of plots, add an empty plot in the last position so
	# that the x-axis get included on the second row of plots
	#ax = plt.subplot2grid((n_row, n_col), (n_row-1,n_col-1))
	#ax.scatter(x=df['Date/Time'], y=df[parameter])

	# Add x-axis sideways
	fig.autofmt_xdate()

	# Save plot to file and close figure
	if cleaned is True:
		filename = 'intro_line_plot.png'
	else:
		filename = 'intro_line_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()