###############################################################################
### Tabel for introdcution section
###############################################################################

### Description:
# ...


#------------------------------------------------------------------------------
### Import packages


#------------------------------------------------------------------------------
### Set variables


#------------------------------------------------------------------------------
### Functions

def intro_count_tabel(df, intro_section_config):

	# Create a dummy tabel_dict
	tabel_dict = {'1': {'QC Comment': 'temp bad', 'Count':'3', 'Percent':'10'},
	'2': {'QC Comment': 'co2 bad', 'Count':'6', 'Percent':'24'},
	'3': {'QC Comment': 'sal bad', 'Count':'1', 'Percent':'9'}}

	return tabel_dict