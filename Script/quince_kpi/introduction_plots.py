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


def intro_plots(intro_plot_config, render_dict, parameters, df, output_dir):

	for kpi_type, config in intro_plot_config.items():
		if config['include']:
			filename = kpi_type + '_filename'
			render_dict[filename] = eval('kpi.'+ kpi_type)(parameters=parameters,
				df=df, output_dir=output_dir, kwargs=config['function_input'])
	return render_dict