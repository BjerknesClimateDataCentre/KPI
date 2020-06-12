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
		eval('kpi.'+ kpi_name)(
			parameter_dict=intro_section_config['parameters'], df=df,
			output_dir=output_dir)

# This function creates and returns the KPI tables for the measured section
def intro_tables(intro_section_config, df):
	intro_tables_dict = {}
	for kpi_name, kpi_config in intro_section_config['kpi_tables'].items():
		table_dict = eval('kpi.' + kpi_name)(df=df,
			parameter_dict=intro_section_config['parameters'])
		intro_tables_dict[kpi_config['number']] = table_dict
	return intro_tables_dict



def eval_intro_fig_function(kpi_name, parameter_dict, df, output_dir):
	eval('kpi.' + kpi_name)(parameter_dict=parameter_dict,
		df=df, output_dir=output_dir)

def eval_intro_tab_function(kpi_name, parameter_dict, df):
	table_dict = eval('kpi.' + kpi_name)(parameter_dict=parameter_dict, df=df)
	return table_dict

# This function creates the KPI figures for measured section, and store
def eval_meas_fig_function(kpi_name, sensor, meas_section_config, df, output_dir):
	eval('kpi.' + kpi_name)(sensor=sensor,
		meas_section_config=meas_section_config, df=df, output_dir=output_dir)

# This function creates and returns the KPI tables for the measured section
def eval_meas_tab_function(kpi_name, sensor, meas_section_config, df):
	table_dict = eval('kpi.' + kpi_name)(sensor=sensor,
		meas_section_config=meas_section_config, df=df)
	return table_dict
