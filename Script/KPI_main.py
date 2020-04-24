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
from jinja2 import FileSystemLoader, Environment
import pdfkit


###----------------------------------------------------------------------------
### Input parameters . MOVE TO CONFIG!
###----------------------------------------------------------------------------

# !!! Need input about for which station(s) and time period!!!
# To be added later.
#--------

# !!! The list of parameters will be extracted from the config file.
# !!! For conveniance, it's done in main script for now.
# Which parameters to check ('True' means all). While writing the this script
# its important to check that the report looks good with varying number of
# parameters.
#parameters = ['Temp [degC]']
#parameters = ['Temp [degC]',
#			 'fCO2 [uatm]']
#parameters = ['Temp [degC]',
#			'fCO2 [uatm]',
#			'Atmospheric Pressure [hPa]',
#			'Instrument Ambient Pressure [hPa]']
#parameters = ['H2O Mole Fraction [umol mol-1]',
#			'Instrument Ambient Pressure [hPa]',
#			'Atmospheric Pressure [hPa]',
#			'Temp [degC]',
#			'CO2 Mole Fraction [umol mol-1]']
#parameters = ['H2O Mole Fraction [umol mol-1]',
#			'Instrument Ambient Pressure [hPa]',
#			'Atmospheric Pressure [hPa]',
#			'Temp [degC]',
#			'CO2 Mole Fraction [umol mol-1]',
#			'fCO2 [uatm]',
#			'Equilibrator Pressure (relative) [hPa]']
#parameters = True


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

# Cleanup old content in output directory
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
intro_plot_config = configs['intro_plot_config']
param_config = configs['param_config']


###---------------------------------------------------------------------------
### Identify / extract / import (???) datasets
###----------------------------------------------------------------------------

# !!! This section cannot be completed before we know how the script will
# extract/receive data from QuinCe.

# !!! Suggestion for import: Create a function which reads all filenames in
# data directory and extracts their vessel and data level info from the
# filename. The functions output is a list of dictionaries with info on which
# files to combine etc. which will be used as loop indexes later when KPIs are
# created.
# -----------

# !!! For now:
# Store the file names from the data direcotry in a list
data_files = os.listdir(data_dir)

# Loop through all files in data directory and read data into 'df'
# !!! Currenlty this only works with one file!
# !!! If more than one file (from the same station): add the df's together
# (NaN's if some cols missing).
for file in data_files:
	data_path = os.path.join(data_dir, file)
	df = pd.read_csv(data_path, low_memory=False)


###---------------------------------------------------------------------------
### Extract basic information from the data frame
###----------------------------------------------------------------------------

# Identify data level from filename
for level in data_levels:
	if level in data_files[0]:
		data_level = level

# Identify station name from filename
for station_name, station_code in station_code.items():
	if station_code in data_files[0]:
		station = station_name

# Set the timestamp column, and extract start and end date
kpi.set_datetime(df)
df_start = df['Date/Time'][0]
df_end = df['Date/Time'][len(df)-1]

# Get all parameters names in df (excludes georef and QC parameters)
# !!! Is this nessesary???
all_parameters = kpi.get_parameters(df)

# Store the basic information extracted above in a dictionary.
# (This dictionary will be filled with information thourghout this script, and
# finally be used as input when the report is created.)
render_dict = {'data_level':data_level, 'station':station, 'df_start':df_start,
			 'df_end':df_end, 'all_parameters':all_parameters}


###----------------------------------------------------------------------------
### Create KPIs
###----------------------------------------------------------------------------

# !!! Remove this when params are extracted from config file
#if parameters is True:
#	parameters = all_parameters

# Exrtract list of parameters to include
parameters = []
for param_name, config in param_config.items():
	if config['include']:
		parameters.append(param_name)


# This function creates the KPI plots for the report introduction, store them
# in the output directory, and stores their filenames in the render dictionary
kpi.intro_plots(intro_plot_config=intro_plot_config, render_dict=render_dict,
	parameters=parameters, df=df, output_dir=output_dir)

# !!! Function for making plots for each parameter chapter


###----------------------------------------------------------------------------
### Create report
###----------------------------------------------------------------------------

# Load the html template
templateLoader = FileSystemLoader("templates")
templateEnv = Environment(loader=templateLoader)
template = templateEnv.get_template("base.html.jinja")

# Create the html string
html_string = template.render(render_dict)

# Write the html string to file and convert to pdf
with open('output/report.html','w') as f:
	f.write(html_string)
pdfkit.from_file('output/report.html', 'output/report.pdf')