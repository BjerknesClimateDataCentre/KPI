###############################################################################
### FUNCTION TO READ AND CLEANUP METADATA FILE FROM THE CP                  ###
###############################################################################

### Description:
# This function reads the file received from the CP containing metadata updates.
# It returns the cleaned up metadata.

# The csv file we get from CP will have headers:
# more....

#------------------------------------------------------------------------------
### IMPORT PACKAGES ###
import csv

#------------------------------------------------------------------------------
### READ THE UPDATES FILE ###

# Read the update file and save the result in 'update_file'.
# Add "newline=''" so that we do not mistake a line break as a new row.

def import_data(filename):
	with open(filename, newline='') as update_file:
		# The csv.DictReader converts lines in the csv file to python
		# dictionaries. The keys are their corresponding header in the first
		# line.
		updates_reader = csv.DictReader(update_file, delimiter=',')
		# Store the dictionaries in a list
		updates=[]
		for row in updates_reader:
			updates.append(row)


	#---------------------------------------------------------------------------
	### ADD THE TYPE USING SPARQL ###



	#---------------------------------------------------------------------------
	### CLEANUP THE UPDATES FILE ###

	# Import to the KPIDB needs to happen in a certain order. E.g. need to
	# import a new person (from 'person' table) before we can import their role
	# (from 'Assumed role' table).

	# The order to sort - by Type - is:
	order_dict = {
		'Person':1,
		'Ship':2,
		'Mooring':3,
		'Station':4,
		'Platform Deployment':5,
		'Assumed Role':6,
		'Value Type':7,
		'Variable':8,
		'Calibration':9,
		'Sensor':10,
		'Instrument':11,
		'Sensor Deployment':12,
		'Instrument Deployment':13}

	# Loop through the list of dictionaries, and add an 'order' key-value.
	# If the 'type' is not in our defined 'order_dict' we do not need this info
	# in the KPIDB, and we assign the order '999' (for easy removal in the next
	# step).
	for dictionary in updates:
		current_type = dictionary["Type"]
		dictionary['order'] = order_dict.get(current_type, 999)

	# Remove the list items where order-value is 999
	updates[:] = [
		dictionary for dictionary in updates if dictionary.get('order') != 999
	]

	# Sort the list items by the order key.
	updates = sorted(updates,key=lambda i:i['order'])

	return updates
