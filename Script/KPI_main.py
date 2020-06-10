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
old_content = os.listdir(output_dir)
for content in old_content:
	os.remove(os.path.join(output_dir, content))


###----------------------------------------------------------------------------
### Extract configurations
###----------------------------------------------------------------------------

# Store configuration variables
with open ('./config.json') as file:
	all_configs = json.load(file)


###---------------------------------------------------------------------------
### Identify / extract / import (???) datasets
###----------------------------------------------------------------------------

# !!! Need input when run script about for which instrument/station and
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
for level in all_configs['data_level_config']:
	if level in data_files[0]:
		data_level = level

# Identify instrument name (full and short) from filename
for instrument, config in all_configs['instrument_config'].items():
	if config['code'] in data_files[0]:
		inst_name_full = instrument
		inst_name_short = config['short_name']
		inst_variables = config['variables']

# Set the timestamp column, and extract start and end date
kpi.set_datetime(df)
df_start = str(df['Date/Time'][0].date())
df_end = str(df['Date/Time'][len(df)-1].date())

# Store the basic information extracted above in the render dictionary. This
# dictionary will be filled with information thourghout this script, and
# finally be used as input when the report is created.
render_dict = {'report_type': sys.argv[1], 'data_filename': file,
	'data_level': data_level, 'inst_name_full': inst_name_full,
	'inst_name_short': inst_name_short, 'df_start': df_start, 'df_end': df_end}


###---------------------------------------------------------------------------
### Create report section configuration dictionaries
###---------------------------------------------------------------------------

#-----------
# INTRO CONFIG

# Create an introduction section configuration dictionary and fill with
# figure filenames and fig/tab numbers
intro_section_config = {}
intro_section_config['kpi_figures'] = kpi.add_filename(
	kpi_dict=all_configs['kpi_config']['intro_figures'], kpi_type='intro',
	short_name='')
returned = kpi.add_number(kpi_dict=intro_section_config['kpi_figures'],
	section_count=1, count=1)
intro_section_config['kpi_figures'] = returned[0]


returned = kpi.add_number(kpi_dict=all_configs['kpi_config']['intro_tables'],
	section_count=1, count=1)
intro_section_config['kpi_tables'] = returned[0]

#-----------
# MEASURED AND CALCULATED CONFIG

# Create config dictionaries for the measured (sensor) and calculated values
meas_section_config = {}
calc_section_config = {}

# For each variable measured by the instrument add all sensors and calc values
# to the dictionaries
for variable in inst_variables:
	variable_dict = all_configs['variable_config'][variable]

	for sensor in variable_dict['sensors']:
		if sensor not in meas_section_config:
			meas_section_config[sensor] = all_configs['vocab_config'][sensor]

	for calc_value in variable_dict['calc_values']:
		if calc_value not in calc_section_config:
			calc_section_config[calc_value] = all_configs['vocab_config'][calc_value]

# For measured variables, add all kpi figure/tables with filenames and number
fig_count = 1
tab_count = 1
for variable, var_config in meas_section_config.items():

	kpi_figures = {}
	for kpi_name in all_configs['kpi_config']['meas_figures'].keys():
		kpi_figures[kpi_name] = {'filename': variable + '_' + kpi_name + '.png'}
		kpi_figures[kpi_name].update({'number': '2.' + str(fig_count)})
		fig_count += 1
	var_config['kpi_figures'] = kpi_figures

	kpi_tables = {}
	for kpi_name in all_configs['kpi_config']['meas_tables'].keys():
		kpi_tables[kpi_name] = {'number': '2.' + str(tab_count)}
		tab_count += 1
	var_config['kpi_tables'] = kpi_tables


# For calculated values, add all kpi figure/tables with filenames and number
fig_count = 1
tab_count = 1
for value, value_config in calc_section_config.items():

	kpi_figures = {}
	for kpi_name in all_configs['kpi_config']['calc_param_figures'].keys():
		kpi_figures[kpi_name] = {'filename': value + '_' + kpi_name + '.png'}
		kpi_figures[kpi_name].update({'number': '3.' + str(fig_count)})
		fig_count += 1
	value_config['kpi_figures'] = kpi_figures

	kpi_tables = {}
	for kpi_name in all_configs['kpi_config']['calc_param_tables'].keys():
		kpi_tables[kpi_name] = {'number': '3.' + str(tab_count)}
		tab_count += 1
	value_config['kpi_tables'] = kpi_tables


#-----------
# Add all parameters ('parameters' are use when there is a mix of sensor and
# calculated values) with their col header name in df and the fig label name
# to the intro config dictionray
intro_section_config['parameters'] = {
	config['col_header_name'] : config['fig_label_name_python']
	for param, config in meas_section_config.items()}
intro_section_config['parameters'].update(
	{config['col_header_name'] : config['fig_label_name_python']
	for param, config in calc_section_config.items()})

## ---------
# Add the section configs to the render dictionary
render_dict.update({'intro_section_config': intro_section_config,
	'meas_section_config': meas_section_config,
	'calc_section_config': calc_section_config})


###----------------------------------------------------------------------------
### Create KPIs
###----------------------------------------------------------------------------

# Create introduction section figures, stored in the output directort
kpi.intro_figures(intro_section_config=intro_section_config, df=df,
	output_dir=output_dir)

# Create introduction section tables and store them in the render dictionary
render_dict['intro_tables'] = kpi.intro_tables(
	intro_section_config=intro_section_config, df=df)

# Create the measured section figures, stored in output directory
kpi.meas_figures(meas_section_config=meas_section_config, df=df,
	output_dir=output_dir)

# Create the measured section tables and store them in the render dictionary
render_dict['meas_tables'] = kpi.meas_tables(
	meas_section_config=meas_section_config, df=df)

# !!! Create the fgures and tables for the calculated parameters section !!!


###----------------------------------------------------------------------------
### Create report
###----------------------------------------------------------------------------


#def clever_function(a, b):
#	sum = a + b
#	return sum

#def clever_function2(a, b):
#	difference = a - b
#	return difference

#render_dict.update({'test_a': 2, 'test_b': 3})

# Load the html template
template_loader = FileSystemLoader("templates")
template_env = Environment(loader=template_loader)
#template_env.globals['clever_function'] = clever_function
#template_env.globals['clever_function2'] = clever_function2
#template_env.globals['intro_figures'] = kpi.intro_figures
template = template_env.get_template("base.html")

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