
# Ontario Birth Study: Email Lifestyle Questionnaires
## Description
As per the study protocol, the Ontario Birth Study distributes Lifestyle  
Questionnaires (LSQ) on a weekly basis. This program is intended to help  
automate the process of sending LSQs to subjects enrolled in the study and  
performs related tasks. Specifically, this program does the following:

1. Get information about which LSQs were completed since the last time the  
script was run using the REDCap API.
2. Update the OBS database with the LSQ completion data.
3. Determine who currently needs REDCap links to access the LSQs. There are two  
categories of subjects who need an LSQ:
    1. Subjects who need to be given an LSQ link based on their gestational age.
    2. Subjects who need to be followed up since they have not completed the LSQ  
    since the last contact.
4. Send and organize the emails containing the LSQ links.
5. Check the Edinburgh Postnatal Depression Scale (EPDS) of recently completed 
LSQs and send a list of subjects who need to be followed up to the OBS Research  
Coordinator. There are two categories of subjects how need to be followed up  
based on their EPDS score:
    1. Subjects who have a high EPDS score.
    2. Subjects who answer affirmatively to 'The thought of harming myself has  
    occured to me'.

## Technologies
Project is created with:
* Python version: 3.9.0
* Microsoft Access version: 2013
* REDCap API
* SQL

## Requirements
* [Python](https://www.python.org/)
* pip (normally installed with Python)
* Windows 10
* Outlook
* access to the Mount Sinai network drive containing OBS materials (e.g. Access  
database)

## Usage
Check out the [documentation](build/html/index.html) for more information about
installation, configuration, and usage.


## Contact
* Feel free to contact me for questions regarding this specific project; however, I am no longer responsible for maintaining it.
* For information about how to access Ontario Birth Study data, you can contactthem through their [website](http://www.ontariobirthstudy.ca).

## License
[MIT](LICENSE.txt)



integration tests vs functional
not really meant for wide distribution; setup is sparse (https://stackoverflow.com/questions/43658870/requirements-txt-vs-setup-py)