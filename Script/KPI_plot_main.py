###############################################################################
###  MAIN SCRIPT FOR MAKING KPI REPORTS                                     ###
###############################################################################


# Description
# ...


###----------------------------------------------------------------------------
### Import packages
###----------------------------------------------------------------------------

import quince_kpi as kpi
import os
import json
import pandas as pd
import jinja2
import pdfkit
import wkhtmltopdf


###----------------------------------------------------------------------------
### Handling directories
###----------------------------------------------------------------------------

# Store path to the main script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Create a data files and output directories if does not exist
directories = ["data_files", "output"]
for directory in directories:
	if not os.path.isdir('./'+ directory):
		os.mkdir(os.path.join(script_dir,directory))

# Store path to the data and output directories
data_dir = os.path.join(script_dir,'data_files')
output_dir = os.path.join(script_dir,'output')

# !! While working on script: Cleanup content in output directory
old_plots = os.listdir(output_dir)
for plot in old_plots:
	os.remove(os.path.join(output_dir, plot))


###----------------------------------------------------------------------------
### Extract information from the config file
###----------------------------------------------------------------------------

with open ('./config.json') as file:
	configs = json.load(file)
station_code = configs['station_code']
data_levels = configs['data_levels']


###---------------------------------------------------------------------------
### Identify / extract / import (???) datasets
###----------------------------------------------------------------------------

# !!! This section cannot be completed before we know how the script will
# extract/receive data from QuinCe.

# !!! Suggestion: Create a function which reads all filenames in data direcotry
# and extracts their vessel and data level info from the filename. Output is a
# list of dictionaries. This will determine how the files are combined and how
# to loop the KPIs plot creations.
#-----------

# !!! For now:
# Store the file names from the data direcotry in a list
data_files = os.listdir(data_dir)

# Loop through all files in data directory and read data into 'df'
# !!! Currenlty this only works with one file!
# !!! If more than one file: add the df's together (NaN's if some cols missing)
for file in data_files:
	data_path = os.path.join(data_dir, file)
	df = pd.read_csv(data_path, low_memory=False)


###---------------------------------------------------------------------------
### Initialise report and add basic information
###----------------------------------------------------------------------------

# Identify data level from filename
for level in data_levels:
	if level in data_files[0]:
		data_level=level

# Identify station name from filename
for station_name, station_code in station_code.items():
	if station_code in data_files[0]:
		station = station_name

# Set the timestamp column, and extract start and end date
kpi.set_datetime(df)
df_start = df['Date/Time'][0]
df_end = df['Date/Time'][len(df)-1]

# Get the parameter names and units for current df
parameters = kpi.get_parameters(df)

#------
#http://zetcode.com/python/jinja/


###----------------------------------------------------------------------------
### KPI: plot data
###---------------------------------------------------------)-------------------

# Plot one variable
#colname = "H2O Mole Fraction [umol mol-1]"
#kpi.show_data(colname=colname, df=df, output_dir=output_dir)


# Plot 'plot_data' KPI for all variables:
#for parameter in parameters:
#	kpi.plot_data(colname=parameter, df=df, output_dir=output_dir, cleaned=True)


###----------------------------------------------------------------------------
### Finalise report
###----------------------------------------------------------------------------

# Create the pdf in the output directory
pdf.output('output/tuto1.pdf', 'F')
