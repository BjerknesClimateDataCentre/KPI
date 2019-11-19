####################################
### IMPORT METADATA TO THE KPIDB ###
####################################

### Description:
# This script reads the file received from the CP (called 'update file') containing
# metadata updates, and imports them to the KPIDB (Key Performanice Indicators Database).

# The csv file we get from CP will have headers:
# Type,id,field,value,link_type,link_id

### How to run the script
# import os
# os.chdir("C:/Users/cla023/MyFiles/Projects/KPI/1.KPIDB/5_Script_metadata_import")
# exec(open("import_metadata_to_KPIDB.py").read())


#---------------------------------------------------------------------------
### IMPORT PACKAGES ###
import os
import quince_kpi



#---------------------------------------------------------------------------
### READ THE UPDATES FILE ###

# Read the update file and save the result in 'update_file'.
# Add "newline=''" so that we do not mistake a line break as a new row.



updates = quince_kpi.import_data(os.path.join(os.path.dirname(os.path.realpath(__file__)),  'updates_testfile.txt'))
print(updates)