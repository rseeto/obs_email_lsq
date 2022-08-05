Installation
============

Confirming Python and pip are installed
---------------------------------------
After installing `Python <https://www.python.org/>`_, you can use 'Windows PowerShell' to confirm both Python and pip, Python's package manager, are installed::
    
    py --version
    py -m pip --version

Downloading repository
----------------------
To run this program, this repository must be cloned or downloaded. The GitHub provided instructions on how to do this are available at `https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository <https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository/>`_.

Creating a virtual environment
------------------------------
It is best practice to create a virtual environment for this project. After you change your working directory to the local copy of this repository in Powershell (e.g. `cd obs_email_lsq`), you can create a virtual environment in the local copy of this repository by entering the following commands::

    py -3 -m venv .venv
    .venv\scripts\activate

If you receive a message that says 'Activate.ps1 is not digitally signed. You cannot run this script on the current system.', it may be necessary to `change the execution policy <https://docs.microsoft.com/en-ca/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2/>`_. For example::

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Installing requirements
-----------------------
Once the virtual environment is created and successfully activiated, the required packages will need to be installed using the following command::

    py -m pip install -r /path/obs_email_lsq/obs_email_lsq/requirements.txt