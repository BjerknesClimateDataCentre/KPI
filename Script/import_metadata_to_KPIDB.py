###############################################################################
### IMPORT METADATA TO THE KPIDB                                            ###
###############################################################################

### Description:
# This script requests for metadata updates from the Carbon Portal, re-arange
# it, and adds it to the KPIDB (Key Performance Indicators Data Base)


#------------------------------------------------------------------------------
### IMPORT PACKAGES ###
import os
import quince_kpi


#------------------------------------------------------------------------------
### REQUEST METADATA UPDATES ###


#------------------------------------------------------------------------------
### READ CLEANED UP METADATA UPDATES ###


updates = quince_kpi.import_data(
	os.path.join(os.path.dirname(os.path.realpath(__file__)),
	'updates_testfile.txt')
)

print(updates)

#------------------------------------------------------------------------------
### ADD UPDATES TO THE KPIDB ###