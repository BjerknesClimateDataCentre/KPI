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
### Extract configurations and create render dictionary
###----------------------------------------------------------------------------

# Store configuration variables
with open ('./config.json') as file:
	all_configs = json.load(file)

with open ('./new_config.json') as new_file:
	all_new_configs = json.load(new_file)

## ---------
# Config cleanup
#-----------

# INTRO CONFIG
# Add filenames to the introduction section figures
intro_config = kpi.add_filename(kpi_dict=all_configs['intro_config'],
	kpi_type='intro', short_name='')

# Add figure numbers to the introduction section
returned = kpi.add_number(kpi_dict=intro_config, section_count=1, count=1)
intro_config = returned[0]

#-----------
# MEASURED PARAMETER CONFIG
# Remove info about measured parameters that will not be included in the report
meas_param_config = kpi.remove_false(d=all_configs['meas_param_config'])

fig_count = 1
tab_count = 1
for param, config in meas_param_config.items():
	# Remove info on figure and tabel kpi's that will not be used in report
	meas_param_config[param]['kpi_figures'] = kpi.remove_false(config['kpi_figures'])
	meas_param_config[param]['kpi_tabels'] = kpi.remove_false(config['kpi_tabels'])

	# Add filenames for figures
	meas_param_config[param]['kpi_figures'] = kpi.add_filename(
		kpi_dict=config['kpi_figures'], kpi_type='parameter',
		short_name=config['short_name'])

	# Add figure numbers
	returned = kpi.add_number(kpi_dict=config['kpi_figures'], section_count=2,
		count=fig_count)
	meas_param_config[param]['kpi_figures'] = returned[0]
	fig_count = returned[1]

	# Add tabel numbers
	returned = kpi.add_number(kpi_dict=config['kpi_tabels'], section_count=2,
		count=tab_count)
	meas_param_config[param]['kpi_tabels'] = returned[0]
	tab_count = returned[1]


#-----------
# CALCULATED PARAMETER CONFIG
# Remove info about calculated parameters that will not be included in the report
calc_param_config =  kpi.remove_false(d=all_configs['calc_param_config'])

# !! add filenames, and fignumbers !! WAIT TILL HAVE CALC KPIS !!

## ---------
# Add the intro and parameter configs to the render dictionary. This dictionary
# will be filled with information thourghout this script, and finally be used
# as input when the report is created.
render_dict = {'intro_config': intro_config,
	'meas_param_config': meas_param_config,
	'calc_param_config': calc_param_config,
	'report_type': sys.argv[1]}


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

# Set the timestamp column, and extract start and end date
kpi.set_datetime(df)
df_start = str(df['Date/Time'][0].date())
df_end = str(df['Date/Time'][len(df)-1].date())

# Store the basic information extracted above in a dictionary.
render_dict.update({'data_filename': file, 'data_level': data_level,
	'inst_name_full': inst_name_full, 'inst_name_short': inst_name_short,
	'df_start': df_start, 'df_end': df_end})


###----------------------------------------------------------------------------
### Create KPIs
###----------------------------------------------------------------------------

#--------------------------
# INTRODUCTION SECTION
# Create the KPI figures (create a parameter
# dictionary which gives the intro_figures function the information about
# the figure label names to use for each paraemters)
parameter_dict = {param : config['fig_label_name_python']
				for param, config in meas_param_config.items()}
parameter_dict.update({param : config['fig_label_name_python']
				for param, config in calc_param_config.items()})
kpi.intro_figures(intro_config=intro_config,
	parameter_dict=parameter_dict, df=df, output_dir=output_dir)

#--------------------------
# MEASURED PARAMETER SECTION
# Create the KPI figures, stored in output directory
kpi.meas_param_figures(meas_param_config=meas_param_config, df=df,
	output_dir=output_dir)

# Create the KPI tabels and store them in the render dictionary
#render_dict['meas_param_tabels_dict'] = kpi.meas_param_tabels(
#	meas_param_config=meas_param_config, df=df)
render_dict['meas_param_tabels_dict'] = kpi.meas_param_tabels(
	meas_param_config=meas_param_config, df=df)
#render_dict['meas_param_tabels_dict'] = meas_param_tabels_dict
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