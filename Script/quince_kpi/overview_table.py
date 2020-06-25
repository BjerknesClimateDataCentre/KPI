###############################################################################
### TABLE FOR OVERVIEW SECTION
###############################################################################

### Description of KPI:
# The kpi function 'overview_count_table' produces a table dictionary with
# an overview of the parameters adressed in the report: their long and short
# name with units, if its measured or calculated, and the number of values


#------------------------------------------------------------------------------
### Import packages


#------------------------------------------------------------------------------
### Declare constants etc.


#------------------------------------------------------------------------------
### Functions

# Create a parameter overview table
def overview_count_table(df, meas_vocab, calc_vocab):
	table_list = []
	for sensor_vocab in meas_vocab.values():
		table_list.append({
			'Parameter': sensor_vocab['subsection_title'],
			'Short Name': sensor_vocab['fig_label_name_html'],
			'Parameter Type': 'Measured',
			'Total Number of Values': len(df[sensor_vocab['col_header_name']])
			})  # Use df.dropna(subset=[...])
	return table_list