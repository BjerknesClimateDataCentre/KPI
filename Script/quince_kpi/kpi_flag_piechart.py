###############################################################################
### KPI: Pie char
###############################################################################

### Description:
# Function for creating a pie chart for a single parameter


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os
import numpy as np

#------------------------------------------------------------------------------
### Set variables
size = 4
color_dict = {'2':'green','3':'orange','4':'red', 'nan':'grey'}

#------------------------------------------------------------------------------
### Functions

def flag_piechart(parameter, short_name, df, output_dir, **kwargs):

	# Store the parameters QC flags in a list (remove '.0' if needed)
	flag_list = list(df[parameter + ' QC Flag'])
	flag_list_cleaned = [str(item).split('.')[0] for item in flag_list]

	# Get the unique flags and their frequencies
	flag_freq = np.unique(flag_list_cleaned, return_counts=True)
	unique_flags = flag_freq[0]
	freq = flag_freq[1]

	# Create color list:
	color_list = []
	for flag in unique_flags:
		color_list.append(color_dict[flag])

	# Create pie chart
	plt.subplots(figsize=(size,size))
	patches, texts = plt.pie(freq, colors=color_list, startangle=90)
	plt.legend(patches, unique_flags, loc="best")
	plt.axis('equal')
	plt.tight_layout()

	# Save the plot to file
	filename = short_name + '_flag_piechart.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')

	return filename