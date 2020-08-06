###############################################################################
### Create param vocabularies for chosen parameters
###############################################################################

### Description:
# Function 'create_vocab' returns a parameter vocabulary for the parameters
# listed in the input 'param_list'. It extracts the requested vocabularies
# (key-value pairs) from the 'vocab_config' (inside 'config.json').

# The function is ran through the 'base.html' template to create report
# section* specific parameter vocabulary dictionaries, which the template
# conveniently can loop through to create a report section. These section
# specific parameter vocabularies are also needed as input to the KPI
# functions.

# *at least used for the report sections 'Measured values' and 'Calculated
# values')

#------------------------------------------------------------------------------
### Import packages


#------------------------------------------------------------------------------
### Set variables


#------------------------------------------------------------------------------
### Functions

# Extract a parameter vocabulary dictionary based on input parameter list
def create_vocab(param_list, vocab_config):
	new_vocab = {}
	for param in param_list:
		new_vocab[param] = vocab_config[param]
	return new_vocab