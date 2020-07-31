
Creating Key Performance Indicators (KPI) Reports for Marine ICOS Data
==========================================================================


### Project Description ###
The Ocean Thematic Centre (OTC) wish to create some Key Performance Indicators
(KPI) reports for the marine ICOS data. These reports will contain various KPI
plots which give insight into how the ICOS stations perform over time. More
specificially, data frequency, how often a sensor fails, quality control (QC)
results, and how QC is performed etc. over various time scales. An exact list
of such KPIs have not yet been decided.

BCDC will setup a system so that various reports based on the KPI plots can be
made on the fly (possibly with an easy to use GUI on the OTC website/jupter
notebook). The reports we have in mind includes (but are not limited to):
* **Station report**: giving insight into how a station has performed in a
specific time period or since entering ICOS. These are of interest to the
station's PIs.
* **Annual report**: showing how the marine stations have perfomed in the last
 year. OTC can include such a report in their annual reports to stakeholders
 like NFR and the Head Office.
* **Sensor report**: combining statistics on a specific sensor type across the
stations. These are relevant for the manufacturers.
* **Country report**: how does the stations from a specific country perform. Of
interest to the countries focal point and their funders.
* **QuinCe report**: can show how people QC their data, and shed light on
weaknesses in the QC system, and possibly detect if QC is not performed in a
standardised way. This is of interest to the OTC and the further software
development.

Initially the focus is on building a system for creating 'Station reports' (as
described above), while keeping in mind that the system should be able to
easily expand to include the other report types in the future. The reports are
made based on QuinCe NRT/L2 export format, containing parameter values,
their QC flag and QC comment(s). Thus the system should also be aligned with
the data structure inside QuinCe (the relationships between and vocabularies
of: instruments, sensors and calculated values).


### Current Status ###
The system can now take in an NRT exported file from QuinCe and build a simple
and clean looking 'Station report' showing what the data looks like, how the data
was flagged by the automatic QC, and which QC comments were assigned.

A lot of work has been put into creating the basic structure of the system.
This is now in place and in accordance with QuinCe and the future expansions
planned (as described above).


### The Road Ahead ###
Work can continue on the 'Station reports'. Minor and major suggested tasks are
listed in the projects Issues section. The major task include adding contents
to the secions 'calculated parameters' and 'property property plots'. (See
description of how to add a new kpi figure or table in the file
[function_template.py](Script/quince_kpi/function_template.py).) Feedback from
PIs (and possibly OTC) would soon be nessecary. Work on expancind the system to
produce other reports types should wait till OTC and PIs are more or less happy
with the 'Station report' type.


### System Description ###
The system is based on the python package Jinja2 which is a temlate language
for python and html (see Jinja2 documentation [here](
https://overiq.com/flask-101/basics-of-jinja-template-language/)).

The main python script [KPI_main.py](Script/KPI_main.py) is ran (inside a
virtual python environment) to create a report. The only input arument is
currently 'HO' or 'PI', which defines the level of descriptions in the
'Station report'. (In the future these input arguments can include e.g.
report type, start and end date.)

The main script imports the data and the configuration file, extracts relevant
information from both, and shares this information and the data file with the
html base template [base.html](Script/templates/base.html). The html base
template: exports the relevant hard coded text from smaller html templates
files; it calls python functions which creates figures and tables; and it uses
macros (equivalent to a function) to add content which is repeated (e.g. adding
all figures to a report section). Finally, the main python script creates the
report as an html string and converts it to pdf format.

See more detailed information inside the individual script files.