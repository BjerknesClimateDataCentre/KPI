
Creating Key Performance Indicators Reports for the marine ICOS data
====================================================================


### Project description ###
The Ocean Thematic Centre (OTC) wish to create some Key Performance Indicators
(KPI) reports for the marine ICOS data. These reports will give some insight
into how the stations, sensors and instruments perform over time. The KPI will
be visualised with plots and tables showing things like data frequency, how
often a sensor fails, QC results, and how QC is performed etc. over various
time scales. An exact list of such KPIs have not yet been decided.

We will setup a system so that various reports based on the KPIs plots can be
made on the fly (possibly with an easy to use GUI on the OTC website/jupter
notebook). The reports we have in mind includes (but are not limited to):
* **station reports**: giving insight into how a station has performed since
entering ICOS. These are of interest to the Station PIs
* **annual reports**: showing how the marine stations have perfomed in the last
 year. OTC can include these in their annual reports to stakeholders such as
 NFR and the Head Office.
* **sensor reports**: combining statistics on a specific sensor type across the
stations. These are relevant for the manufacturers.
* **country reports**: how does the stations from a specific counry perform. Of
interest to the countries focal point and their funders.
* **QuinCe report**: can show how people QC their data, and shed light on
weaknesses in the QC system, and possibly detect if QC is not performed in a
similar way. This is of interest to the OTC and the further software
development.

Initially the focus is on building a system for creating 'station reports' (as
described above), while keeping in mind that the system should be able to
easily expand to include the other report types in the future. The reports are
made based on QuinCe NRT/L2 export format, containing parameter values,
their QC flag and QC comment(s). Thus the system should also be inligned with
the data structure inside QuinCe (the relationships between and vocabularies
of: instruments, sensors and calculated values).


### Current Status ###
The system can now take in an NRT exported file from QuinCe and build a simple
and clean looking station report showing what the data looks like, how the data
was flagged by the automatic QC, and which QC comments were assigned.

A lot of work has been put into creating the basic structure of the system.
This is now in place and in accordance with QuinCe and the future expansions
planned (as described above). See how the system is build in the figure
'filename'.


### The road ahead ###
Work can continue on the 'station reports'. Minor and major suggested tasks are
listed in githubs issues section. The major task include adding contents to the
secions 'calculated parameters' and 'property property plots'. Feedback from
PIs (and possibly OTC) would soon be nessecary. Work on expancind the system to
produce other reports types should wait OTC and PIs are more or less happy with
the station report type.


### System description ###
The system is based on the python package Jinja2 which is a temlate language
for python and html (see Jinja2 documentation [here](https://overiq.com/flask-101/basics-of-jinja-template-language/).

The main python script [KPI_main.py](Script/KPI_main.py) is ran (inside a
virtual python environment) to create the report. The only input arument is
currently 'HO' or 'PI', which defines the level of descriptions in the report.
(In the future these input arguments can include e.g. report type, start and
end date.)

The main script imports the data and the configuration file, extracts relevant
information from both, and shares this information and the data frame with the
html base template [base.html](Script/templates/base.html). The html base
template: exports the relevant hard coded text from smaller html templates
files; it calls python functions which creates figures and tables; and it uses
macros (equivalent to a function) to add content which is repeated (e.g. adding
all figures to a report section). Finally, the main script creates the report
as an html string and converts it to pdf format.

See more detialed information inside the individual script files.