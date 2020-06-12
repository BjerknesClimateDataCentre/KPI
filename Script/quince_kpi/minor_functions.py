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

# Extract a list of parameters from a dataframe (NOT CURRENTLY IN USE)
def get_parameters(df):
	column_names = list(df.columns)
	georefs = ['Date/Time', 'Latitude', 'Longitude', 'Depth [m]']

	parameters = []
	for column in column_names:
		if column not in georefs and 'QC' not in column:
			parameters.append(column)
	return parameters