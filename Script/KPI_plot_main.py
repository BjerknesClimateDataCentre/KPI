###############################################################################
###  MAIN SCRIPT FOR MAKING KPI PLOTS                                       ###
###############################################################################


# Description
# ...


###----------------------------------------------------------------------------
### Import packages
###----------------------------------------------------------------------------

import quince_kpi as kpi
import os
import pandas as pd

###----------------------------------------------------------------------------
### Handling directories
###----------------------------------------------------------------------------

# Store path to the main script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Create a data directory if it does not already exist
if not os.path.isdir('./data_files'):
	os.mkdir(os.path.join(script_dir,'data_files'))

# Store path to the data directory
data_dir = os.path.join(script_dir,'data_files')


###----------------------------------------------------------------------------
### Identify datasets
###----------------------------------------------------------------------------

# !!! Create a function which reads all filenames in data direcotry and
# extracts their vessel and data level info from the filename. Output is a list
# of dictionaries. This will determine how the files are combined and how to
# loop the KPIs plot creations.

# Store the file names from the data direcotry in a list
data_files = os.listdir(data_dir)


###----------------------------------------------------------------------------
### Import data, set date time, and extract parameters
###----------------------------------------------------------------------------

# Loop through all files in data directory and read data into 'df'
for file in data_files:
	data_path = os.path.join(data_dir, file)
	df = pd.read_csv(data_path, low_memory=False)

# Set the timestamp column
kpi.set_datetime(df)

# Get the parameter names and units for current df
parameters = kpi.get_parameters(df)


###----------------------------------------------------------------------------
### Make KPI plots
###----------------------------------------------------------------------------

