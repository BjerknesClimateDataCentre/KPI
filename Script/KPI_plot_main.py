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
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns    # Do I need this???


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
# !!! If more than one file: add the df's together (NaN's if some cols missing)
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

#-------------
# USefull stuff:
#--------

# Get all unique values for a column:
# df['Colname'].unique()

# Remove rows with NaN/'empty'
# df = df.dropna(subset=['pCO2 [uatm]'])

# Group data:
# group_by_QCFlag = df.groupby(by=['colname QC Flag'])

# Get average and count after grouping:
# flag_average = group_by_QCFlag.mean()
# flag_count = group_by_QCFlag.count()

# Plot function - plot() with parameters:
# kind - bar, barh, pie, scatter, kde
# color - in hex codes
# linestyle - solid, dotted, dashed
# xlim, ylim
# legend - true or false
# labels - list corresponding to the number of cols in data frame
# title - a string
#------------



# Plot one variable

df_pco2_noNaN = df.dropna(subset=['pCO2 [uatm]'])
df_pco2_noNaN.plot(kind='scatter', y='pCO2 [uatm]', x='Date/Time')
plt.savefig(output_dir + '/pco2.png')





