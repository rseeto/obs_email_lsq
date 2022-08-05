Usage
=====

This program is intended to be run on a weekly basis. As a result, the 'Task Scheduler' can be used to automate the running of this script. This can be done by creating a 'Basic Task' using the 'Create Basic Task Wizard'. 

* From the 'Trigger' section of the wizard, choose the day, time and frequency to start the script.
* Create a `bat` script with the following information::

    C:\path_to_virtualenv\Scripts\Activate.ps1 && C:\path_to_virtualenv\Scripts\python.exe path_to_python_script.py

* From the 'Action' section of the wizard, select 'Start a program'.
* Enter the following information:
    * Program/script: Path to the previously created `bat` script
    * Start in (optional): Path to this program's folder (e.g. 'T:\\Dept ObGyn Research\\Ontario Birth Study\\OBS scripts\\Python\obs_email_lsq\\obs_email_lsq')