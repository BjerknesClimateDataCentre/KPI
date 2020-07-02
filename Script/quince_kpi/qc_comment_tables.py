###############################################################################
### TABLE(S) SHOWING QC COMMENTS
###############################################################################

### Description of the KPI functions:
# - 'meas_qc_comment_table' creates a table showing counts of various QC
# Comments assigned to a parameter (sensor) by the automatic QC.


#------------------------------------------------------------------------------
### Import packages
import numpy as np


#------------------------------------------------------------------------------
### Declare constants etc.


#------------------------------------------------------------------------------
### Functions

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


def calc_qc_comment_table(parameter, vocab, df):

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