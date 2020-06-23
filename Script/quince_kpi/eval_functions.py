###############################################################################
### FUNCTIONS WHICH RUNS OTHER FUNCTIONS THAT CREATES THE FIGURES AND TABLES
###############################################################################

### Description:
# The functions below (called 'eval functions') are simply running the other
# functions which creates KPI tables and figures (called 'kpi functions').
# The reason for this inbetween-step is that the python function 'eval' (which
# is needed since the we change the function name inside a for loop) is not
# allowed inside the html base template (where this mentioned for loop is
# located). The html base template instead calls these eval functions.

# The input to the eval functions are the name of a kpi, and whatever other
# inputs that kpi function needs. The eval functions calls the kpi functions by
# using the python function 'eval' to create a function name from the combined
# string 'kpi.' (name of the package containig the kpi functions) and the kpi
# name (name of the kpi function).

# There are separate eval functions for creating figures and tabels. This is
# due to the difference in how a table and figure are stored and used after
# they've been created. The eval function running a kpi function which creates
# a figure returnes nothing since the figure is simply stored in the output
# directory (which is later fetched by the html base template based on its
# filename (which again is based on the kpi_name and possibly parameter name)).
# On the other hand, the eval function running a kpi function which creates a
# table returns the table in a dictionary format (which is then transformed
# to html inside the html base template).

# There are also separate eval functions for the different report sections.
# This is related to how the kpi functions for the differen sections often
# have different input requirements.


#------------------------------------------------------------------------------
### Import packages
import quince_kpi as kpi


#------------------------------------------------------------------------------
### Functions

# Run a kpi function which creates a figure for the intro section
def eval_intro_fig_function(kpi_name, meas_vocab, calc_vocab, df, output_dir):
	eval('kpi.' + kpi_name)(meas_vocab=meas_vocab, calc_vocab=calc_vocab,
		df=df, output_dir=output_dir)

# Run a kpi function which creates and returns a table for the intro section
def eval_intro_tab_function(kpi_name, meas_vocab, calc_vocab, df):
	table_list = eval('kpi.' + kpi_name)(meas_vocab=meas_vocab,
		calc_vocab=calc_vocab, df=df)
	return table_list

# Run a kpi function which creates a figure for the measured/calculated value
# sections. (Note: the diagnostics section can likely use this function too.)
def eval_fig_function(kpi_name, param, vocab, df, output_dir):
	eval('kpi.' + kpi_name)(param=param, vocab=vocab, df=df,
		output_dir=output_dir)

# Run a kpi function which creates and returns a table for the
# measured/calculated value sections. (Note: the diagnostics section can likely
# use this function too.)
def eval_tab_function(kpi_name, param, vocab, df):
	table_list = eval('kpi.' + kpi_name)(param=param, vocab=vocab, df=df)
	return table_list