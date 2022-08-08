
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

## Project Organization

    ├── LICENSE
    ├── README.md
    ├── setup.py
    ├── requirements.txt
    ├── docs
    │   ├── build
    │   │   ├── html
    │   │   │   ├── configuration.html
    │   │   │   ├── index.html 
    │   │   │   ├── installation.html
    │   │   │   └── usage.html
    │   │   └── text
    │   │       ├── configuration.text
    │   │       ├── index.text 
    │   │       ├── installation.text
    │   │       └── usage.text
    │   ├── source
    │   ├── make.bat
    │   └── Makefile
    ├── obs_email_lsq
    │   ├── __init__.py
    │   ├── config.py
    │   ├── main.py
    │   ├── obs_data.py
    │   ├── obs_email.py
    │   └── obs_lsq_epds.py
    └── tests
        ├── __init__.py
        ├── test_obs_data.py
        ├── test_obs_email.py
        ├── test_obs_lsq_epds.py
        └── test_results.xml
* Some generated files (i.e. Sphinx) are excluded from the project organization chart

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
Check out the documentation ([html](docs/build/html/index.html), [text](docs/build/text/index.txt)) for more information about 
installation ([html](docs/build/html/installation.html), [text](docs/build/text/installation.txt)), configuration ([html](docs/build/html/configuration.html), [text](docs/build/text/configuration.txt)), and usage ([html](docs/build/html/usage.html), [text](docs/build/text/usage.txt)).


## Contact
* Feel free to contact me for questions regarding this specific project; 
however, I am no longer responsible for maintaining it.
* For information about how to access Ontario Birth Study data, you can contact
them through their [website](http://www.ontariobirthstudy.ca).

## License
[MIT](LICENSE.txt)