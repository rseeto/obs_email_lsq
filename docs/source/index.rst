.. OBS Email LSQs documentation master file, created by
   sphinx-quickstart on Fri Aug  5 12:33:26 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OBS Email LSQs' documentation
==============================
As per the study protocol, the Ontario Birth Study distributes Lifestyle  
Questionnaires (LSQ) on a weekly basis. This program is intended to help  
automate the process of sending LSQs to subjects enrolled in the study and  
performs related tasks. Specifically, this program does the following:

1. Get information about which LSQs were completed since the last time the script was run using the REDCap API.
2. Update the OBS database with the LSQ completion data.
3. Determine who currently needs REDCap links to access the LSQs. There are two categories of subjects who need an LSQ:
   
   A. Subjects who need to be given an LSQ link based on their gestational age.
   B. Subjects who need to be followed up since they have not completed the LSQ since the last contact.

4. Send and organize the emails containing the LSQ links.
5. Check the Edinburgh Postnatal Depression Scale (EPDS) of recently completed LSQs and send a list of subjects who need to be followed up to the OBS Research Coordinator. There are two categories of subjects how need to be followed up based on their EPDS score:
   
   1. Subjects who have a high EPDS score.
   2. Subjects who answer affirmatively to 'The thought of harming myself has occured to me'.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Contents
--------
   
.. toctree::
   
   installation
   configuration
   usage