###############################################################################
### Title
###############################################################################

### Description:
# ...


#------------------------------------------------------------------------------
### Import packages


#------------------------------------------------------------------------------
### Set variables


#------------------------------------------------------------------------------
### Functions




""" HOW TO ADD A NEW KPI FIGURE OR TABLE TO THE REPORT:
 - Copy this template file and give it a reasonable filename (if relevant
 include report section name to be consistent)
 - Inside the new file create a function that produces the new figure or table
 - Add the new filename and function name to the __init__.py file
 - Add the function name to the 'kpi_config' in the configuration file. This
 config dictionary shows which kpi functions to run for each of the report
 sections
 - Create two new kpi description files in the folder
 templates/kpi_description. One description is uesd in the text of the report,
 the other used as the figure or table caption. Naming of these files must
 follow the principle '*kpi_name*_*text/caption*.html'.

 Note that a function creating a figure need to store the figure as png inside
 the output directory in order for the report template to find it. While a
 function creating a table need to return the table in the following format(
 list of dictionary where each dictionary represents one row in table):
 table_list = [
 	{header1: value, header2: value, etc.},
 	{header1: value, header2: value, etc.}
 ]
"""