###############################################################################
### Functions doing minor things                                            ###
###############################################################################

### Description:
# ...


#------------------------------------------------------------------------------
import pandas as pd

# Set the date time column in a dataframe
def set_datetime(df):
	df.loc[:,'Date/Time'] = pd.to_datetime(
		df.loc[:,'Date/Time'], format = '%Y-%m-%dT%H:%M:%S.%fZ')

# Extract a list of parameters from a dataframe
def get_parameters(df):
	column_names = list(df.columns)
	georefs = ['Date/Time', 'Latitude', 'Longitude', 'Depth [m]']

	parameters = []
	for column in column_names:
		if column not in georefs and 'QC' not in column:
			parameters.append(column)
	return parameters

# Remove key-value pairs from dict where the value 'include' is set to false
def remove_false(d):
	d = {k : v for k, v in d.items() if v['include']}
	return d

# Go through a kpi dictionary and add filename
def add_filename(kpi_dict, kpi_type, short_name):
	for kpi_name, kpi_config in kpi_dict.items():
		if kpi_type == 'intro':
			filename = kpi_name + '.png'
		else:
			filename = short_name + '_' + kpi_name + '.png'
		kpi_dict[kpi_name]['filename'] = filename
	return kpi_dict

# Go through a kpi dictionary and add figure/table number
def add_number(kpi_dict, section_count, count):
	for kpi_name, kpi_config in kpi_dict.items():
		kpi_dict[kpi_name]['number'] = str(section_count) + '.' +  str(count)
		count += 1
	return [kpi_dict, count]