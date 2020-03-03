###############################################################################
###  MAIN SCRIPT FOR MAKING KPI REPORTS                                     ###
###############################################################################


# Description
# ...

###----------------------------------------------------------------------------
### Input parameters
###----------------------------------------------------------------------------

# !!! Need input about for which stations and time period!!! To be added later.
#--------

# The following parameters show which kpi's to run and for which columns (list
# of columnnames, or 'True' if want to run for all columns)
#kpi_line_plot = ['H2O Mole Fraction [umol mol-1]',
#			'Instrument Ambient Pressure [hPa]',
#			'Atmospheric Pressure [hPa]']#,
#			'Temp [degC]',
#			'CO2 Mole Fraction [umol mol-1]']
kpi_line_plot = ['H2O Mole Fraction [umol mol-1]']
#kpi_line_plot = True

#kpi_line_plot_cleaned = ['H2O Mole Fraction [umol mol-1]',
#			'Instrument Ambient Pressure [hPa]',
#			'Atmospheric Pressure [hPa]',
#			'Temp [degC]',
#			'CO2 Mole Fraction [umol mol-1]']
#kpi_line_plot_cleaned = ['H2O Mole Fraction [umol mol-1]']
#kpi_line_plot_cleaned = True



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

# Store path to the data and output directories, and the css path.
data_dir = os.path.join(script_dir,'data_files')
output_dir = os.path.join(script_dir,'output')
css_path = os.path.join(script_dir,'templates') + '\\style.css'

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
### Extract basic information from the data frame
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
all_parameters = kpi.get_parameters(df)

# Create a dictionary which will be filled with information used in the report
render_dict = {'css_path':css_path, 'data_level':data_level, 'station':station, 'df_start':df_start,
			 'df_end':df_end, 'all_parameters':all_parameters}


###----------------------------------------------------------------------------
### KPI: plot data
###----------------------------------------------------------------------------

if 'kpi_line_plot' in globals():
	if kpi_line_plot is True:
		kpi_line_plot = all_parameters
	render_dict['kpi_line_plot_filename'] = kpi.line_plot(
		colnames=kpi_line_plot, df=df, output_dir=output_dir)

if 'kpi_line_plot_cleaned' in globals():
	if kpi_line_plot_cleaned is True:
		kpi_line_plot_cleaned = all_parameters
	render_dict['kpi_line_plot_cleaned_filename'] = kpi.line_plot(
		colnames=kpi_line_plot_cleaned, df=df, output_dir=output_dir,
		cleaned=True)


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


# LEs denne!
#https://jinja.palletsprojects.com/en/2.11.x/templates/

