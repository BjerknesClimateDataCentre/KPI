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
	table_list = []
	for sensor_vocab in meas_vocab.values():
		table_list.append({
			'Parameter': sensor_vocab['subsection_title'],
			'Short Name': sensor_vocab['fig_label_name_html'],
			'Parameter Type': 'Measured',
			'Total Number of Values': len(df[sensor_vocab['col_header_name']])
			})
	return table_list