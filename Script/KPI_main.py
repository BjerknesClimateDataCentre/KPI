###############################################################################
###  SCRIPT FOR CREATING A KPI REPORT
###############################################################################

# Description:
# What the script does:
# - Imports the data and the the configuration file.
# - Use the data and configurations to create a render dictionary containing
# all information relevant for the report.
# - Feed the data and render dictionary to the html template ('base.html'). The
# outcome of this is an html string.
# - Converted the html string to a pdf.

# Requiremens:
# - The command line arguments required when running the script is report type
# (either 'PI' or 'HO') which determines the amount of descriptions in the
# report.
# - The package 'quince_kpi' must be in the same directory as this script.
# - The 'templates' folder which contains all html related files must be in the
# same directory as this script.
# - A data file (in QuinCe export format) inside the 'data_files' folder in the
# same directory as this script. (This is a temporary solution. The plan is
# that the script will fetch data directly from QuinCe based on instrument and
# date information given in the command line arguments.)

# Outputs (stored in the output folder):
# - The report (.pdf and .html).
# - Report figures (.png).
# - The render dictionary (.json; for convenience while developing)


###----------------------------------------------------------------------------
### Import packages
###----------------------------------------------------------------------------

import os
import sys
import pandas as pd
import json
from jinja2 import FileSystemLoader, Environment
import quince_kpi as kpi
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
old_content = os.listdir(output_dir)
for content in old_content:
	os.remove(os.path.join(output_dir, content))


###----------------------------------------------------------------------------
### Import dataset(s) and configuration file
###----------------------------------------------------------------------------

# Loop through all files in data directory and read data into 'df'
# Note: Currently the script can only deal with one input data file, but future
# plan is to concatenate df's if more than one file from the same instrument.
data_files = os.listdir(data_dir)
for data_file in data_files:
	data_path = os.path.join(data_dir, data_file)
	df = pd.read_csv(data_path, low_memory=False)

# Extract configuration file
with open ('./config.json') as config_file:
	all_configs = json.load(config_file)


###----------------------------------------------------------------------------
### Extract relevant info from data and configuration
###----------------------------------------------------------------------------

# Identify data level from the filename
for level in all_configs['data_level_config']:
	if level in data_files[0]:
		data_level = level

# Set the timestamp column, and extract start and end date
df.loc[:,'Date/Time'] = pd.to_datetime(
	df.loc[:,'Date/Time'], format = '%Y-%m-%dT%H:%M:%S.%fZ')
df_start = str(df['Date/Time'][0].date())
df_end = str(df['Date/Time'][len(df)-1].date())

# Store all data related info in data_config
data_config = {'data_filename': data_file, 'data_level': data_level,
	'df_start': df_start,'df_end': df_end}

###---------------
# Identify instrument name (full and short) from filename
for instrument, config in all_configs['instrument_config'].items():
	if config['code'] in data_files[0]:
		inst_name_full = instrument
		inst_name_short = config['short_name']
		inst_variables = config['variables']

# Create a dictionary of instrument namings
inst_config = {'inst_name_full': inst_name_full,
	'inst_name_short': inst_name_short}

###---------------
# Create parameter lists for the measured (sensor) and calculated values.
# For each variable measured by the instrument add all sensors and calculated
# values to the lists.
meas_param = []
calc_param = []
for variable in inst_variables:
	variable_dict = all_configs['variable_config'][variable]
	for sensor in variable_dict['sensors']:
		if sensor not in meas_param:
			meas_param.append(sensor)
	for calc_value in variable_dict['calc_values']:
		if calc_value not in calc_param:
			calc_param.append(calc_value)

# Create customised vocab config to only include parameters from the measured
# and calculated parameter lists
custom_vocab_config = {}
for param in meas_param:
	custom_vocab_config[param] = all_configs['vocab_config'][param]
for param in calc_param:
	custom_vocab_config[param] = all_configs['vocab_config'][param]


###---------------
# Add relevant prop-prop-plot KPI names to the prop-prop_config list
custom_prop_config = {}
# Add deltaT KPI to prop list if Temp at equilibrator is measured
Teq_header_name = all_configs['vocab_config']['Teq']['col_header_name']
if not df[Teq_header_name].isnull().all():
	custom_prop_config['deltaT'] = all_configs['prop_config']['deltaT']

# Add x and y axis prop-prop parameters to the custom_vocab_config if not there
for prop_config in all_configs['prop_config'].values():
	x_param = prop_config['x-axis']
	if x_param not in custom_vocab_config.keys():
		custom_vocab_config[x_param] = all_configs['vocab_config'][x_param]
	y_param = prop_config['y-axis']
	if y_param not in custom_vocab_config.keys():
		custom_vocab_config[y_param] = all_configs['vocab_config'][y_param]

###---------------
# Create the render dictionary and store the report type, output directory
# and other configurations extracted above
render_dict = {'report_type': sys.argv[1], 'output_dir': output_dir,
	'inst_config': inst_config, 'data_config': data_config,
	'section_config': all_configs['section_config'], 'meas_param': meas_param,
	'calc_param': calc_param, 'custom_prop_config': custom_prop_config,
	'custom_vocab_config': custom_vocab_config}


###----------------------------------------------------------------------------
### Create report
###----------------------------------------------------------------------------

# Load the html template, and share the data frame and kpi package with the
# jinja environment
template_loader = FileSystemLoader("templates")
template_env = Environment(loader=template_loader, trim_blocks=True,
	lstrip_blocks=True)
template_env.globals['kpi'] = kpi
template_env.globals['df'] = df
template = template_env.get_template("base.html")

# Create the html string and write to file
html_string = template.render(render_dict)
report_path = """output/DataQualityReport_{inst}_{start}-{end}""".format(
	inst=inst_name_short, start=str(df_start.replace('-', '')),
	end=str(df_end.replace('-', '')))
with open(report_path + '.html','w') as html_file:
	html_file.write(html_string)

# Convert html string to pdf
options = {'margin-top': '0.75in', 'margin-right': '0.75in',
	'margin-bottom': '0.75in', 'margin-left': '0.75in',
	'footer-right': '[page]'}
pdfkit.from_file(report_path + '.html', report_path + '.pdf', options=options)


###----------------------------------------------------------------------------
### Export render dictionary to json file (convenient while developing scripts)
###----------------------------------------------------------------------------

with open('output/render_dict.json', 'w') as render_file:
	json.dump(render_dict, render_file, indent=4, separators=(',', ': '))