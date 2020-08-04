###############################################################################
### TIMELINE SHOWING QC COMMENTS
###############################################################################

###  Description
# The function 'qc_comment_timeline' creates a timeline showing when the
# various qc comments occur for a given parameter.


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os


#------------------------------------------------------------------------------
### Set variables

# Figure sizes
FIG_WIDTH = 8
FIG_HEIGHT = 3


#------------------------------------------------------------------------------
### Functions

def qc_comment_timeline(parameter, vocab, df, output_dir):


	# Set up the figure
	fig, ax = plt.subplots(figsize=(FIG_WIDTH,FIG_HEIGHT))

	plt.plot(df['Date/Time'], df[vocab[parameter]['col_header_name']])

	# Save figure to file and close figure
	filename = parameter + '_qc_comment_timeline.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()