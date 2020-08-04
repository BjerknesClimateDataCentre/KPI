###############################################################################
### PIECHART SHOWING DISTRIBUTION OF FLAGS
###############################################################################

### Description of the KPI functions:
# - 'flag_piechart' creates a pie chart showing flag distribution for a
# single parameter (sensor).


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os
import numpy as np


#------------------------------------------------------------------------------
### Declare constants etc.

# Figure sizes
PIE_FIG_SIZE = 2.5

# Specify the color representing each QC flag (and missing value)
COLOR_DICT = {'2':'#85C0F9','3':'#A95AA1','4':'#F5793A', 'nan':'grey'}


#------------------------------------------------------------------------------
### Functions

# Create a piechart showing the distribution of flags for a given sensor
def flag_piechart(parameter, vocab, df, output_dir):

	# Store the parameter QC flags in a list (remove '.0')
	col_header_name = vocab[parameter]['col_header_name']
	flag_list = list(df[col_header_name + ' QC Flag'])
	flag_list_cleaned = [str(item).split('.')[0] for item in flag_list]

	# Get the unique flags and their frequencies (as arrays)
	unique_flags, freq = np.unique(flag_list_cleaned, return_counts=True)

	# Create color list according to the color dictionary
	color_list = []
	for flag in list(unique_flags):
		if flag == 'nan':
			color_list.append('grey')
		else:
			color_list.append(COLOR_DICT[flag])

	# Create pie chart
	plt.subplots(figsize=(PIE_FIG_SIZE,PIE_FIG_SIZE))
	patches, text, autotexts = plt.pie(freq, colors=color_list, startangle=90,
		autopct='%1.0f%%')
	for autotext in autotexts:
		autotext.set_color('white')
	plt.legend(patches, list(unique_flags), loc="best")
	plt.axis('equal')
	plt.tight_layout()

	# Save figure to file and close figure
	filename = parameter + '_flag_piechart.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()