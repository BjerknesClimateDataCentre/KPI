###############################################################################
###                                                                         ###
###############################################################################

### Description:
#

#------------------------------------------------------------------------------
#import pandas as pd
import matplotlib.pyplot as plt
import os


# Function plots a parameter vs time and saves plot in output directory
def plot_data(colname, df, output_dir, cleaned=False):
	# Remove rows with NaNs
	df = df.dropna(subset=[colname])

	# Identify the parameters QC flag columns and set the color code
	color_column = colname + ' QC Flag'

	# Setup the plot
	fig, ax = plt.subplots()

	# If cleaned is false, plot all data. Else, only plot data with QC flag 2.
	if cleaned is False:
		# Set plot color for the QC flags, and add to plot in a loop
		color_code = {2:'green',3:'orange',4:'red'}
		for flag, col in color_code.items():
			limited_df = df[df[color_column]==flag]
			ax.scatter(x=limited_df['Date/Time'], y=limited_df[colname],
				c=col, label=flag, alpha=0.7, edgecolors='none', marker='.')
		ax.legend()

	else:
		limited_df = df[df[color_column]==2]
		ax.scatter(x=limited_df['Date/Time'], y=limited_df[colname],
			c='green', alpha=0.7, edgecolors='none', marker='.')

	# Make axis sideways, add axis labels and grid
	fig.autofmt_xdate()
	plt.xlabel('Date/Time', fontsize=13)
	plt.ylabel(colname, fontsize=13)
	ax.grid(True)

	# Save plot to file
	filename = colname.split(' [')[0] + '.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath)