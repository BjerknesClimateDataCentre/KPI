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
import numpy as np
import string


#------------------------------------------------------------------------------
### Set variables

# Figure sizes
FIG_WIDTH = 9
SUBPLOT_HEIGHT = 1.3

# Title fontsize:
TITLE_FONTSIZE = 9

# Specify the plot marker color
MARKER_COL = '#F5793A'

#------------------------------------------------------------------------------
### Functions

def qc_comment_timeline(parameter, vocab, df, output_dir):

	# Create list of unique QC comments for the given parameter (remove nan,
	# and split if more than one comment in a row)
	qc_comment_header = vocab[parameter]['col_header_name'] + ' QC Comment'
	unique_comments_raw = np.unique(list(df[qc_comment_header]))
	unique_comments_noNan = [x for x in unique_comments_raw if x != 'nan']
	comment_list = []
	for comment in unique_comments_noNan:
		if ';' in comment:
			splitted = comment.split(';')
			for split in splitted:
				comment_list.append(split.lstrip())
		else:
			comment_list.append(comment)
	comment_list = np.unique(comment_list)

	# Set up the figure, with one subplot per QC comment
	n_plots = len(comment_list)
	fig_height = SUBPLOT_HEIGHT * n_plots
	fig, axs = plt.subplots(nrows=n_plots, ncols=1, sharex=True, sharey=True,
		figsize=(FIG_WIDTH,fig_height))

	# Adjust height between subplots to make space for subplot titles
	plt.subplots_adjust(hspace=0.5)

	# Add subplots to figure in a loop
	subplot_count = 0
	for comment in comment_list:

		# Set the axes for the plot
		ax = axs[subplot_count]

		# Extract data frame rows where QC comment field contains the 'comment'
		df_edit = df[df[qc_comment_header].str.contains(comment, na=False)]

		# Add subplot
		ax.plot(df_edit['Date/Time'],
			df_edit[vocab[parameter]['col_header_name']], marker='v',
			linestyle='None', c=MARKER_COL)

		# Add grid and subplot title
		ax.grid(True)
		title = '{letter})     \'{comment}\''.format(
			letter=string.ascii_lowercase[subplot_count], comment=comment)
		ax.set_title(title, loc='left', fontsize=TITLE_FONTSIZE,
			fontweight='bold')

		# Increase subplot counter
		subplot_count += 1
		if subplot_count == n_plots:
			break

	# Add y and x label
	fig.autofmt_xdate()
	fig.text(0.05, 0.5, vocab[parameter]['fig_label_name_python'],
		verticalalignment='center', rotation='vertical')

	# Save figure to file and close figure
	filename = parameter + '_qc_comment_timeline.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()