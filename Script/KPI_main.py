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
### Extract configurations and create render dictionary
###----------------------------------------------------------------------------

# Store configuration variables
with open ('./config.json') as file:
	configs = json.load(file)
station_code = configs['station_code']
data_levels = configs['data_levels']
intro_config = configs['intro_config']
param_config = configs['param_config']
kpi_config = configs['kpi_config']

## ---------
# Intro and param config cleanup

# Removes info about intro kpi's that will not be included in the report
intro_config = kpi.remove_false(d=intro_config)

# Add filename and figure number for the introduction chapter figures
intro_config = kpi.add_filename_fignumber(kpi_dict=intro_config,
	kpi_type='intro', chapter_count=1, short_name='')

# Remove info about parameters that will not be included in the report
param_config = kpi.remove_false(d=param_config)

# Remove info about parameter kpis that will not be included in the report, and
# add filename and figure number for the parameter chapters figures
chapter_count = 2
for param, config in param_config.items():
	param_config[param]['kpis'] = kpi.remove_false(config['kpis'])
	param_config[param]['kpis'] = kpi.add_filename_fignumber(kpi_dict=config['kpis'],
		kpi_type='parameter', short_name=config['short_name'],
		chapter_count=chapter_count)
	chapter_count += 1

## ---------
# Add the intro and parameter configs to the render dictionary. This dictionary
# will be filled with information thourghout this script, and finally be used
# as input when the report is created.
render_dict = {'intro_config': intro_config, 'param_config': param_config,
	'kpi_config': kpi_config}


###---------------------------------------------------------------------------
### Identify / extract / import (???) datasets
###----------------------------------------------------------------------------

# !!! Need input in config file about for which station(s) and time period!!!
# To be added later.

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
df_start = str(df['Date/Time'][0].date())
df_end = str(df['Date/Time'][len(df)-1].date())

# Get all parameters names in df (excludes georef and QC parameters)
# !!! Is this nessesary???
all_parameters = kpi.get_parameters(df)

# Store the basic information extracted above in a dictionary.
render_dict.update({'data_filename': file, 'data_level':data_level,
			'station':station, 'df_start':df_start, 'df_end':df_end})


###----------------------------------------------------------------------------
### Create KPIs
###----------------------------------------------------------------------------

# Create the KPI figures for the report introduction
parameters = list(param_config.keys())
kpi.intro_plots(intro_config=intro_config, parameters=parameters,
	df=df, output_dir=output_dir)

# Create the KPI plots for the individual parameter sections in the report
kpi.meas_param_plots(param_config=param_config, parameters=parameters, df=df,
	output_dir=output_dir)

print(render_dict)


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
options = {'margin-top': '0.75in', 'margin-right': '0.75in',
	'margin-bottom': '0.75in', 'margin-left': '0.75in'}
pdfkit.from_file('output/report.html', 'output/report.pdf', options=options)