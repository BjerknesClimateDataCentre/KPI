###############################################################################
###                                                                         ###
###############################################################################

### Description:
#

#------------------------------------------------------------------------------
#import pandas as pd
import matplotlib.pyplot as plt
import os
#from mlxtend.plotting import category_scatter


# Function plots parameter(s) vs time and saves plot in output directory
def show_data(colname, df, output_dir):
	# Remove rows with NaNs
	df = df.dropna(subset=[colname])

	# Identify the parameters QC flag columns and set the color code
	color_column = colname + ' QC Flag'
	color_code = {2:'green',3:'orange',4:'red'}

	# Plot in a loop, one QC flag at the time
	fig, ax = plt.subplots()
	for flag, col in color_code.items():
		limited_df = df[df[color_column]==flag]
		ax.scatter(x=limited_df['Date/Time'], y=limited_df[colname],
		c=col, label=flag, alpha=0.7, edgecolors='none', marker='.')

	# Make axis sideways
	fig.autofmt_xdate()

	# Add axis labels, grid and legend
	plt.xlabel('Date/Time', fontsize=13)
	plt.ylabel(colname, fontsize=13)
	ax.grid(True)
	ax.legend()

	# Save plot to file
	filename = colname.split(' [')[0] + '.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath)