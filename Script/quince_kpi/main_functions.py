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

# This function creates the KPI plots for the report introduction, and store
# them in the output directory
def intro_plots(intro_config, parameter_dict, df, output_dir):
	for kpi_name, config in intro_config.items():
		eval('kpi.'+ kpi_name)(parameter_dict=parameter_dict, df=df,
			output_dir=output_dir, kwargs=config['function_input'])


# This function creates the KPI plots for parameter sections, and store
# them in the output directory
def meas_param_plots(meas_param_config, df, output_dir):
	for parameter, config in meas_param_config.items():
		for kpi_name in config['kpi_figures']:
			eval('kpi.' + kpi_name)(parameter=parameter, df=df,
				meas_param_config=meas_param_config, output_dir=output_dir)