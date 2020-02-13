###############################################################################
###                                                             ###
###############################################################################

### Description:
#

#------------------------------------------------------------------------------
import pandas as pd

def set_datetime(df):
	df.loc[:,'Date/Time'] = pd.to_datetime(
		df.loc[:,'Date/Time'], format = '%Y-%m-%dT%H:%M:%S.%fZ')


def get_parameters(df):
	column_names = list(df.columns)
	georefs = ['Date/Time', 'Latitude', 'Longitude', 'Depth [m]']

	parameters = []
	for column in column_names:
		if column not in georefs and 'QC' not in column:
			parameters.append(column)

	# If want to return a dictiornay where parameters and units are separate
	#parameters = {}
	#for column in column_names:
	#	if column not in georefs and 'QC' not in column:
	#		name = column.split(' [')[0]
	#		unit = column.split(' [')[1][:-1]
	#		parameters[name] = unit

	return parameters

