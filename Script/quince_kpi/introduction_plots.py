###############################################################################
### Function for creating introduction plots                                ###
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
def intro_plots(intro_plot_config, parameters, df, output_dir):
	for kpi_name, config in intro_plot_config.items():
		eval('kpi.'+ kpi_name)(parameters=parameters, df=df,
			output_dir=output_dir, kwargs=config['function_input'])