###############################################################################
### TABLE FOR OVERVIEW SECTION
###############################################################################

### Description of KPI:
# ...


#------------------------------------------------------------------------------
### Import packages


#------------------------------------------------------------------------------
### Declare constants etc.


#------------------------------------------------------------------------------
### Functions

def overview_count_table(df, meas_vocab, calc_vocab):
	table_list = []
	for sensor_vocab in meas_vocab.values():
		table_list.append({
			'Parameter': sensor_vocab['subsection_title'],
			'Short Name': sensor_vocab['fig_label_name_html'],
			'Parameter Type': 'Measured',
			'Total Number of Values': len(df[sensor_vocab['col_header_name']])
			})
	return table_list