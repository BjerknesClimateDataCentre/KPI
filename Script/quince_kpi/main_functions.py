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
	table_list = eval('kpi.' + kpi_name)(meas_vocab=meas_vocab,
		calc_vocab=calc_vocab, df=df)
	return table_list

# Creates a KPI figure for the measured section and store it in the output dir
# !!! Only pass in vocab, can take meas and calc.
# !!! Diagnostics can also be created with this one
def eval_meas_fig_function(kpi_name, sensor, meas_vocab, df, output_dir):
	eval('kpi.' + kpi_name)(sensor=sensor,
		meas_vocab=meas_vocab, df=df, output_dir=output_dir)

# Create and return a KPI table for the measured section
def eval_meas_tab_function(kpi_name, sensor, meas_vocab, df):
	table_list = eval('kpi.' + kpi_name)(sensor=sensor,
		meas_vocab=meas_vocab, df=df)
	return table_list

# Note:
# - For similar functions for the calculated values secion reuse the
# 'eval_meas_fig_function' and 'eval_meas_tab_function', but edit name,
# and change the 'meas_vocab' input to simply 'vocab'. In that way the
# measured section can use the meas_vocab, and the calculated section can
# use the 'calc_meas' as vocab.
# - The diagnostics plots can also be created with these.!
# - For prop-prop plots send x and y vocab.