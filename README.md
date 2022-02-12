
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

## Installation
### Confirming Python and pip are installed
After installing [Python](https://www.python.org/), you can use 'Windows PowerShell' to confirm both Python  
and pip, Python's package manager, are installed.
```powershell
py --version
py -m pip --version
```
### Downloading repository
To run this program, this repository must be cloned or downloaded. The GitHub  
provided instructions on how to do this are available [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

### Creating a virtual environment
It is best practice to create a virtual environment for this project. After you  
change your working directory to the local copy of this repository in Powershell  
(e.g. `cd obs_email_lsq`), you can create a virtual environment in the local  
copy of this repository by entering the following commands.
```powershell
py -3 -m venv .venv
.venv\scripts\activate
```

If you receive a message that says 'Activate.ps1 is not digitally signed. You  
cannot run this script on the current system.', it may be necessary to [change  
the execution policy](https://docs.microsoft.com/en-ca/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2). For example:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Installing requirements
Once the virtual environment is created and successfully activiated, the  
required packages will need to be installed using the following command.
```powershell
py -m pip install -r /path/obs_email_lsq/obs_email_lsq/requirements.txt
```

## Configuration
You will need to make appropriate changes in the `config.py` file. The contact  
email addresses and paths for the patient contact information, LSQ passwords,  
and the Access database will likely need to be changed. In addition, you will  
need to create a file called `obs_email_lsq/obs_email_lsq/config_api.py`. This  
file should contain a dictionary with the APIs of the associated LSQs. The API  
information should be available from the current institution hosting the REDCap  
instance. At the time of writing, the OBS LSQs were hosted at the [Applied  
Health Research Centre](https://www.hubresearch.ca/). An example of the `config_api.py` is below:

```python
redcap_api = {
    'lsq1': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    'lsq2': 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'lsq3': 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC'   
}
```

## Usage
This program is intended to be run on a weekly basis. As a result, the 'Task  
Scheduler' can be used to automate the running of this script.This can be done  
by creating a 'Basic Task' using the 'Create Basic Task Wizard'. 
* From the 'Trigger' section of the wizard, choose the day, time and frequency  
to start the script.
* Create a `bat` script with the following information:
```bat
C:\path_to_virtualenv\Scripts\Activate.ps1 && C:\path_to_virtualenv\Scripts\python.exe path_to_python_script.py
```
* From the 'Action' section of the wizard, select 'Start a program'
* Enter the following information:
    * Program/script: Path to the previously created `bat` script
    * Start in (optional): Path to this program's folder (e.g.  
    'T:\Dept ObGyn Research\Ontario Birth Study\OBS scripts\Python\obs_email_lsq\obs_email_lsq')

## Contact
* Feel free to contact me for questions regarding this specific project; however, I am no longer responsible for maintaining it.
* For information about how to access Ontario Birth Study data, you can contact them through their [website](http://www.ontariobirthstudy.ca).

## License
[MIT](LICENSE.txt)



integration tests vs functional