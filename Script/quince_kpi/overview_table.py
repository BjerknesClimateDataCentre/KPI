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


# Create a table with overview of parameters evaluated in the reports
def overview_table(df, meas_vocab, calc_vocab):

	# Loops through each parameter and adds a row to the table list
	def add_rows(table_list, vocab, type):
		for param_vocab in vocab.values():
			label = param_vocab['fig_label_name_html']
			if '[' in label:
				short_name = list(label.split(' ['))[0]
				unit = list(label.split(' ['))[1].replace(']','')
			else:
				short_name = label
				unit = '-'
			table_list.append({
				'Parameter': param_vocab['subsection_title'],
				'Short Name': short_name,
				'Unit': unit,
				'Type': type,
				'Number of Data Points':
					len(df.dropna(subset=[param_vocab['col_header_name']]))
			})
		return table_list

	table_list = []
	table_list = add_rows(table_list=table_list, vocab=meas_vocab, type='Measured')
	table_list = add_rows(table_list=table_list, vocab=calc_vocab, type='Calculated')

	return table_list