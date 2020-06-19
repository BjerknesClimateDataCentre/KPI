###############################################################################
### table for introdcution section
###############################################################################

### Description:
# ...


#------------------------------------------------------------------------------
### Import packages


#------------------------------------------------------------------------------
### Set variables


#------------------------------------------------------------------------------
### Functions

def intro_count_table(df, meas_vocab, calc_vocab):

	table_dict = {}
	row_count = 1
	for sensor_vocab in meas_vocab.values():
		table_dict[row_count] = {
			'Parameter': sensor_vocab['subsection_title'],
			'Short Name': sensor_vocab['fig_label_name_html'],
			'Parameter Type': 'Measured',
			'Total Number of Values': len(df[sensor_vocab['col_header_name']])
			}
		row_count += 1

	print(table_dict)
	# Create a dummy table_dict
	#table_dict = {'1': {'Col1 Name': 'value', 'Col2 Name':'value', 'Col3 Name':'value'},
	#'2': {'Col1 Name': 'value', 'Col2 Name':'value', 'Col3 Name':'value'},
	#'3': {'Col1 Name': 'value', 'Col2 Name':'value', 'Col3 Name':'value'}}

	return table_dict