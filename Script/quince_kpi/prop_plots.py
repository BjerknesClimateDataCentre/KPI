###############################################################################
### Functions creating property-property plots
###############################################################################

### Description:
# ...


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os


#------------------------------------------------------------------------------
### Set variables

# Set figure size
FIG_SIZE = 4

# Set plot marker color
MARKER_COL = 'black'


#------------------------------------------------------------------------------
### Functions

# Create the delta T prop prop plot
def deltaT(vocab, prop_config, df, output_dir):

	# Set up the figure
	fig, ax = plt.subplots(figsize=(FIG_SIZE,FIG_SIZE))

	# Extract column header names from function input configs and plot
	x_header = vocab[prop_config['x-axis']]['col_header_name']
	y_header = vocab[prop_config['y-axis']]['col_header_name']
	ax.scatter(df[x_header],df[y_header], marker='.', c=MARKER_COL)

	# Add grid and axis labels
	ax.grid(True)
	plt.xlabel(vocab[prop_config['x-axis']]['fig_label_name_python'])
	plt.ylabel(vocab[prop_config['y-axis']]['fig_label_name_python'])

	# Save the plot to file and close figure
	filename = 'deltaT.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()