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

# Create a table with overview of parameters evaluated in the reports, their
# long and short names, and number of measurements/calculated values
def overview_count_table(df, meas_vocab, calc_vocab):

	# Loop through each parameter and add element (row) to the table list
	table_list = []
	for vocab in meas_vocab.values():
		table_list.append({
			'Parameter': vocab['subsection_title'],
			'Short Name [Unit]': vocab['fig_label_name_html'],
			'Type': 'Measured',
			'Number of Measurements/Values':
				len(df.dropna(subset=[vocab['col_header_name']]))
		})
	for vocab in calc_vocab.values():
		table_list.append({
			'Parameter': vocab['subsection_title'],
			'Short Name [Unit]': vocab['fig_label_name_html'],
			'Type': 'Calculated',
			'Number of Measurements/Values':
				len(df.dropna(subset=[vocab['col_header_name']]))
		})

	return table_list