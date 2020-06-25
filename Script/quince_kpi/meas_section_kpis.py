###############################################################################
### FIGURES AND TABLE(S) FOR THE MEASURED SECTION
###############################################################################

### Description of the KPI functions:
# - 'meas_flag_piechart' creates a pie chart showing flag distribution for a
# single parameter (sensor).
# - 'meas_line_plot' creates a figure with two subplots, one showing all
# measurements from one parameter (sensor), the other plot scaled to improve
# visibility in cases of very high/low valus. We use the following method to
# define the upper and lower cutoffs for this scaling: "The IQR can be used to
# identify outlier by defining limits on the sample values that are a factor k
# of the IQR below the 25th percentile or above the 75th percentile. The common
# value for the factor k is the value 1.5." (https://machinelearningmastery.
# com/how-to-use-statistics-to-identify-outliers-in-data/).
# - 'meas_qc_comment_table' creates a table showing counts of various QC
# Comments assigned to a parameter (sensor) by the automatic QC.


#------------------------------------------------------------------------------
### Import packages
import matplotlib.pyplot as plt
import os
import numpy as np


#------------------------------------------------------------------------------
### Declare constants etc.

# Figure sizes
PIE_FIG_SIZE = 2.5
LINE_FIG_WIDTH = 9
LINE_FIG_HEIGHT = 4.5

# Plot symbol alpha (related to transparency)
ALPHA = 1

# Specify the color representing each QC flag (and missing value)
COLOR_DICT = {'2':'#85C0F9','3':'#A95AA1','4':'#F5793A', 'nan':'grey'}
CONTRAST_COLOR = '#0F2080'

# Title fontsize:
TITLE_FONTSIZE = 9

# Factor to multiply with IQR's to define upper and lower y-range in line plot
K = 1.5


#------------------------------------------------------------------------------
### Functions

# Create a piechart showing the distribution of flags for a given sensor
def meas_flag_piechart(parameter, vocab, df, output_dir):

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
	filename = parameter + '_meas_flag_piechart.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()

# Make a subplot for the meas_line_plot figure
def make_plot(df, col_header_name, ax):

	# Remove NaNs from color_dict since missing values are not plotted
	color_dict_noNan = COLOR_DICT
	if 'nan' in COLOR_DICT:
		color_dict_noNan.pop('nan')

	# Create subplot in loop - one flag at the time
	for flag, col in color_dict_noNan.items():
		df_edit = df[df[col_header_name + ' QC Flag']==int(flag)]
		ax.scatter(x=df_edit['Date/Time'], y=df_edit[col_header_name],
					c=col, label=flag, alpha=ALPHA, edgecolors='none',
					marker='.')

# Creates figure with two subplots for a parameter (sensor), one with all
# measurements, the other scaled
def meas_line_plot(parameter, vocab, df, output_dir):

	# Remove rows where parameter value is missing
	col_header_name = vocab[parameter]['col_header_name']
	df = df.dropna(subset=[col_header_name])

	# Calculate the IQR, cutoffs, and the lower and upper ranges
	q25 = np.percentile(df.loc[:,col_header_name], 25)
	q75 = np.percentile(df.loc[:,col_header_name], 75)
	iqr = q75 - q25
	cut_off = iqr * K
	lower = q25 - cut_off
	upper = q75 + cut_off

	# Set up the figure
	fig, ax = plt.subplots(figsize=(LINE_FIG_WIDTH,LINE_FIG_HEIGHT))

	# Create the first subplot with all values (colored by QC flag)
	ax = plt.subplot2grid((2, 1), (0,0))
	make_plot(df=df, col_header_name=col_header_name, ax=ax)

	# Add the lower and upper cut-off lines to subplotplot
	plt.axhline(y=upper, color=CONTRAST_COLOR, linestyle='-')
	plt.axhline(y=lower, color=CONTRAST_COLOR, linestyle='-')

	# Add grid, axis labels and letter
	ax.grid(True)
	plt.ylabel(vocab[parameter]['fig_label_name_python'])
	ax.set_title('a)', loc='left', fontsize=TITLE_FONTSIZE, fontweight='bold')

	# Create the second plot removing values outside upper and lower range
	ax = plt.subplot2grid((2, 1), (1,0))
	df_scaled = df[(df[col_header_name] > lower)
		& (df[col_header_name] < upper)]
	make_plot(df=df_scaled, col_header_name=col_header_name, ax=ax)

	# Add grid, labels and letter
	ax.legend()
	ax.grid(True)
	fig.autofmt_xdate()
	ax.set_title('b)', loc='left', fontsize=TITLE_FONTSIZE, fontweight='bold')

	# Save the plot to file and close figure
	filename = parameter + '_meas_line_plot.png'
	filepath = os.path.join(output_dir, filename)
	plt.savefig(filepath, bbox_inches='tight')
	plt.close()


def meas_qc_comment_table(parameter, vocab, df):

	# Store the parameter QC comments in a list and remove nan's
	col_header_name = vocab[parameter]['col_header_name']
	comment_list = list(df[col_header_name + ' QC Comment'])
	comment_list = [x for x in comment_list if x == x]

	# Split comments if they contain ';' (means more than one comment in a row)
	comment_list_cleaned = []
	for comment in comment_list:
		if ';' in comment:
			splitted = comment.split('; ')
			comment_list_cleaned.extend(splitted)
		else:
			comment_list_cleaned.append(comment)

	# Extract unique comments and their frequency and store in a dictonary
	unique_comments, freq = np.unique(comment_list_cleaned, return_counts=True)
	table_dict = dict(zip(list(unique_comments), list(freq)))

	# Sort dictionary by the frequency, high to low.
	table_dict_sorted = {k: v for k, v in sorted(table_dict.items(),
		key=lambda item: item[1], reverse=True)}

	# Restructure dict to table format and add percentages to each count
	table_list = []
	for key, value in table_dict_sorted.items():
		percent = round((value/df.shape[0])*100,2)
		table_list.append({'QC Comment': key,
			'Counts': str(value) + ' (' + str(percent) + '%)'})

	return table_list
