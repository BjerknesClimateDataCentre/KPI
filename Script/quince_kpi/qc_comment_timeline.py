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
import pandas as pd
import math


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

	# Create a dummy value to use in subplot then an error occur without any
	# parameter value (e.g. for errors related to missing values). This dummy
	# value needs to be within the subplot y ranges (subplots share an y-axis),
	# so we can use the parameter mean value for all rows with a QC comment.
	df_comment = df[df[qc_comment_header].notnull()]
	dummy_value = np.nanmean(df_comment[vocab[parameter]['col_header_name']])

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

		# The subplot above will not show when errors related to missing values
		# occur, since there is no value to plot. Therefore, plot the dummy
		# value instead for such missing data errors. Create a list contaning
		# the dummy value in locations where the parameter value is missing in
		# the data frame - otherwise set this list value to None. Combine the
		# 'Date/Time' and dummy list into a dummy dataframe and plot it in the
		# current subplot.
		dummy_list = []
		value_list = list(df_edit[vocab[parameter]['col_header_name']])
		for value in value_list:
			if math.isnan(value):
				dummy_list.append(dummy_value)
			else:
				dummy_list.append(None)
		dummy_df = pd.DataFrame()
		dummy_df['Date/Time']  = list(df_edit['Date/Time'])
		dummy_df['dummy_values'] = dummy_list
		ax.plot(dummy_df['Date/Time'], dummy_df['dummy_values'],
			marker='v', linestyle='None', c='blue')

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