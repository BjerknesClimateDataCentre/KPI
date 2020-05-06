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

with open ('./config.json') as file:
	configs = json.load(file)
station_code = configs['station_code']
data_levels = configs['data_levels']
intro_plot_config_full = configs['intro_plot_config']
param_config_full = configs['param_config']
figcaptions = configs['figcaptions']

## ---------
# Extract only relevant information from the intro plot configuration
intro_plot_config_short = {k : v for k, v in intro_plot_config_full.items() if v['include']}

# Add filename of the figure that will be created and its figure number to be
# used in the report (always in section 1 in report, so start with '1.').
intro_plot_count = 1
intro_plot_config = intro_plot_config_short
for kpi_name, config in intro_plot_config_short.items():
	intro_plot_config[kpi_name]['filename'] = kpi_name + '.png'
	intro_plot_config[kpi_name]['fignumber'] = '1.' + str(intro_plot_count)
	intro_plot_count += 1

## ---------
# Extract only relevant information from the parameter configuration

# Remove parameters not to be include in report from the param_config dict
param_config_short = { k : v for k, v in param_config_full.items() if v['include']}

# Loop through each parameter in the param_config dict and remove kpis where
# include is set to 'false'. For kpis with 'include' set to true, add the
# filename of the figure that will be created, and its figure number to be used
# in the report
chapter_count = 2
param_config = param_config_short
for param, config in param_config_short.items():
	fig_count = 1
	for kpi_name, kpi_dict in config['kpis'].items():
		if kpi_dict['include'] is True:
			filename = config['short_name'] + '_' + kpi_name + '.png'
			param_config[param]['kpis'][kpi_name]['filename'] = filename
			param_config[param]['kpis'][kpi_name]['fignumber'] = str(chapter_count) + '.' + str(fig_count)
		fig_count += 1
	chapter_count += 1

## ---------
# Add certain configs to the render dictionary.
# (This dictionary will be filled with information thourghout this script, and
# finally be used as input when the report is created.)
render_dict = {'intro_plot_config': intro_plot_config,
	'param_config': param_config, 'figcaptions': figcaptions}


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

# This function creates the KPI plots for the report introduction, and store
# them in the output directory
parameters = list(param_config.keys())
kpi.intro_plots(intro_plot_config=intro_plot_config, parameters=parameters,
	df=df, output_dir=output_dir)


# Function for making pie charts for each parameter chapter
for parameter, config in param_config.items():
	short_name = config['short_name']
	kpi.flag_piechart(parameter=parameter, short_name=short_name,
		df=df, output_dir=output_dir)


# Function for plotting the data for all parameters
#parameter = "Temp [degC]"
for parameter, config in param_config.items():
	short_name = config['short_name']
	kpi.single_line_plot(parameter=parameter, short_name=short_name,
	df=df, output_dir=output_dir)


#print(render_dict)


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