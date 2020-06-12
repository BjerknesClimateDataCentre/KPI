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

# Creates a KPI figure for the intro section and store it in the output dir
def eval_intro_fig_function(kpi_name, meas_vocab, calc_vocab, df, output_dir):
	eval('kpi.' + kpi_name)(meas_vocab=meas_vocab, calc_vocab=calc_vocab,
		df=df, output_dir=output_dir)

# Ccreate and return a KPI table for the measured section
def eval_intro_tab_function(kpi_name, meas_vocab, calc_vocab, df):
	table_dict = eval('kpi.' + kpi_name)(meas_vocab=meas_vocab,
	calc_vocab=calc_vocab, df=df)
	return table_dict

# Creates a KPI figure for the measured section and store it in the output dir
def eval_meas_fig_function(kpi_name, sensor, meas_vocab, df, output_dir):
	eval('kpi.' + kpi_name)(sensor=sensor,
		meas_vocab=meas_vocab, df=df, output_dir=output_dir)

# Ccreate and return a KPI table for the measured section
def eval_meas_tab_function(kpi_name, sensor, meas_vocab, df):
	table_dict = eval('kpi.' + kpi_name)(sensor=sensor,
		meas_vocab=meas_vocab, df=df)
	return table_dict
