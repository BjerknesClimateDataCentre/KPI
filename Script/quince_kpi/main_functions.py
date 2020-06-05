###############################################################################
### Functions running the kpi functions and producing kpi plots/tables etc. ###
###############################################################################

### Description:
# ...


#------------------------------------------------------------------------------
### Import packages
import quince_kpi as kpi


#------------------------------------------------------------------------------
### Functions

# This function creates the KPI figures for the report introduction, and store
# them in the output directory
def intro_figures(intro_section_config, df, output_dir):
	for kpi_name in intro_section_config['kpi_figures'].keys():
		eval('kpi.'+ kpi_name)(parameter_dict=intro_section_config['parameters'], df=df,
			output_dir=output_dir)

# This function creates and returns the KPI tabels for the measured section
def intro_tabels(intro_section_config, df):
	intro_tabels_dict = {}
	for kpi_name, kpi_config in intro_section_config['kpi_tabels'].items():
		tabel_dict = eval('kpi.' + kpi_name)(df=df,
			intro_section_config=intro_section_config)
		intro_tabels_dict[kpi_config['number']] = tabel_dict
	return intro_tabels_dict


# This function creates the KPI figures for parameter sections, and store
# them in the output directory
def meas_figures(meas_section_config, df, output_dir):
	for parameter, config in meas_section_config.items():
		for kpi_name in config['kpi_figures']:
			eval('kpi.' + kpi_name)(parameter=parameter, df=df,
				meas_section_config=meas_section_config, output_dir=output_dir)

# This function creates and returns the KPI tabels for the measured section
def meas_tabels(meas_section_config, df):
	meas_tabels_dict = {}
	for parameter, config in meas_section_config.items():
		for kpi_name, kpi_config in config['kpi_tabels'].items():
			tabel_dict = eval('kpi.' + kpi_name)(parameter=parameter, df=df,
				meas_section_config=meas_section_config)
			meas_tabels_dict[kpi_config['number']] = tabel_dict
	return meas_tabels_dict