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


# Function plots parameter(s) vs time and saves plot(s) in output directory
def plot_data(colnames, df, output_dir, cleaned=False):

	# List of letters used for labelling the plots
	letters=list(string.ascii_lowercase[0:len(colnames)])
	letter_count = 0

	# Create the filepaths list which will be returned
	filenames = []
	for colname in colnames:

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
			ax.legend(fontsize=11)


		else:
			limited_df = df[df[color_column]==2]
			ax.scatter(x=limited_df['Date/Time'], y=limited_df[colname],
				c='green', alpha=0.7, edgecolors='none', marker='.')

		# Make axis sideways, add axis labels, grid and lettering
		fig.autofmt_xdate()
		plt.xlabel('Date/Time', fontsize=13)
		plt.ylabel(colname, fontsize=13)
		ax.grid(True)
		if len(colnames) > 1:
			ax.set_title(letters[letter_count] + ')', loc='left', fontsize=15,
				fontweight="bold")

		# Save plot to file
		if cleaned is True:
			filename = colname.split(' [')[0] + '_cleaned.png'
		else:
			filename = colname.split(' [')[0] + '.png'
		filename = filename.replace(' ','_')
		filepath = os.path.join(output_dir, filename)
		plt.savefig(filepath)

		# Add filepath to paths list and increase letter counter
		filenames.append(filename)
		letter_count += 1

	return filenames