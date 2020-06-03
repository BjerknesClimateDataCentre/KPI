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
import sys


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
### Extract configurations
###----------------------------------------------------------------------------

# Store configuration variables
with open ('./config.json') as file:
	all_configs = json.load(file)


###---------------------------------------------------------------------------
### Identify / extract / import (???) datasets
###----------------------------------------------------------------------------

# !!! Need input in config file about for which instrument/station and
# time period!!! To be added later.

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
# !!! If more than one file (from the same instrument): add the df's together
# (NaN's if some cols missing).
for file in data_files:
	data_path = os.path.join(data_dir, file)
	df = pd.read_csv(data_path, low_memory=False)


###---------------------------------------------------------------------------
### Extract basic information from the data frame
###----------------------------------------------------------------------------

# Identify data level from filename
for level in all_configs['data_levels']:
	if level in data_files[0]:
		data_level = level

# Identify instrument name (full and short) from filename
for instrument, config in all_configs['instruments'].items():
	if config['code'] in data_files[0]:
		inst_name_full = instrument
		inst_name_short = config['short_name']
		inst_variables = config['variables']

# Set the timestamp column, and extract start and end date
kpi.set_datetime(df)
df_start = str(df['Date/Time'][0].date())
df_end = str(df['Date/Time'][len(df)-1].date())

# Store the basic information extracted above in a dictionary.
render_dict = {'report_type': sys.argv[1], 'data_filename': file,
	'data_level': data_level, 'inst_name_full': inst_name_full,
	'inst_name_short': inst_name_short, 'df_start': df_start, 'df_end': df_end}


###---------------------------------------------------------------------------
### Config cleanup
###---------------------------------------------------------------------------

# INTRO CONFIG
# Add filenames to the introduction section figures
intro_config = kpi.add_filename(kpi_dict=all_configs['all_kpis']['intro_figures'],
	kpi_type='intro', short_name='')

# Add figure numbers to the introduction section
returned = kpi.add_number(kpi_dict=intro_config, section_count=1, count=1)
intro_config = returned[0]

#-----------
# MEASURED PARAMETER CONFIG

# Create config dictionaries for the measured (sensor) and calculated values
meas_param_config = {}
calc_param_config = {}

# For each variable measured by the instrument add all sensors and calc values
# to the dictionaries
for variable in inst_variables:
	variable_dict = all_configs['variable_config'][variable]

	for sensor in variable_dict['sensors']:
		if sensor not in meas_param_config:
			meas_param_config[sensor] = all_configs['data_vocabulary_config'][sensor]

	for calc_value in variable_dict['calc_values']:
		if calc_value not in calc_param_config:
			calc_param_config[calc_value] = all_configs['data_vocabulary_config'][calc_value]

# For measured variables, add all kpi figure/tabels with filenames and number
fig_count = 1
tab_count = 1
for variable, var_config in meas_param_config.items():

	kpi_figures = {}
	for kpi_name in all_configs['all_kpis']['meas_param_figures'].keys():
		kpi_figures[kpi_name] = {'filename': variable + '_' + kpi_name + '.png'}
		kpi_figures[kpi_name].update({'number': '2.' + str(fig_count)})
		fig_count += 1
	var_config['kpi_figures'] = kpi_figures

	kpi_tabels = {}
	for kpi_name in all_configs['all_kpis']['meas_param_tabels'].keys():
		kpi_tabels[kpi_name] = {'number': '2.' + str(tab_count)}
		tab_count += 1
	var_config['kpi_tabels'] = kpi_tabels


# For calculated values, add all kpi figure/tabels with filenames and number
fig_count = 1
tab_count = 1
for value, value_config in calc_param_config.items():

	kpi_figures = {}
	for kpi_name in all_configs['all_kpis']['calc_param_figures'].keys():
		kpi_figures[kpi_name] = {'filename': value + '_' + kpi_name + '.png'}
		kpi_figures[kpi_name].update({'number': '3.' + str(fig_count)})
		fig_count += 1
	value_config['kpi_figures'] = kpi_figures

	kpi_tabels = {}
	for kpi_name in all_configs['all_kpis']['calc_param_tabels'].keys():
		kpi_tabels[kpi_name] = {'number': '3.' + str(tab_count)}
		tab_count += 1
	value_config['kpi_tabels'] = kpi_tabels

## ---------
# Add the intro and parameter configs to the render dictionary. This dictionary
# will be filled with information thourghout this script, and finally be used
# as input when the report is created.
render_dict.update({'intro_config': intro_config,
	'meas_param_config': meas_param_config,
	'calc_param_config': calc_param_config})


###----------------------------------------------------------------------------
### Create KPIs
###----------------------------------------------------------------------------

#--------------------------
# INTRODUCTION SECTION
# Create the KPI figures (create a parameter
# dictionary which gives the intro_figures function the information about
# the figure label names to use for each paraemters)
parameter_dict = {config['col_header_name'] : config['fig_label_name_python']
				for param, config in meas_param_config.items()}
parameter_dict.update({config['col_header_name'] : config['fig_label_name_python']
				for param, config in calc_param_config.items()})
kpi.intro_figures(intro_config=intro_config,
	parameter_dict=parameter_dict, df=df, output_dir=output_dir)

#--------------------------
# MEASURED PARAMETER SECTION
# Create the KPI figures, stored in output directory
kpi.meas_param_figures(meas_param_config=meas_param_config, df=df,
	output_dir=output_dir)

# Create the KPI tabels and store them in the render dictionary
render_dict['meas_param_tabels_dict'] = kpi.meas_param_tabels(
	meas_param_config=meas_param_config, df=df)

#--------------------------
# CALCULATED PARAMETER SECTION

# !!! Create the KPI figures and tables for the calculated parameters section !!!


###----------------------------------------------------------------------------
### Create report
###----------------------------------------------------------------------------

# Load the html template
templateLoader = FileSystemLoader("templates")
templateEnv = Environment(loader=templateLoader)
template = templateEnv.get_template("base.html")

# Create the html string
html_string = template.render(render_dict)

# Write the html string to file and convert to pdf
with open('output/report.html','w') as f:
	f.write(html_string)
options = {'margin-top': '0.75in', 'margin-right': '0.75in',
	'margin-bottom': '0.75in', 'margin-left': '0.75in',
	'footer-right': '[page]'}
pdfkit.from_file('output/report.html', 'output/report.pdf', options=options)



# -------------------------
#!!! While working on this script, export the render dict to a json file
# for easy reading !!!
with open('output/render_dict.json', 'w') as file:
	json.dump(render_dict, file, indent=4,
		separators=(',', ': '))