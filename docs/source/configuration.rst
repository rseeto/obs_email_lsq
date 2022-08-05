Configuration
=============

You will need to make appropriate changes in the `config.py` file. The contact email addresses and paths for the patient contact information, LSQ passwords, and the Access database will likely need to be changed. Object definitions and default values are as follows:

`NOTIFICATION_EMAIL`
    email address(es) of OBS staff notified when after the emails are sent. ::

        NOTIFICATION_EMAIL = 'ryan.seeto@sinaihealth.ca; ryan.seeto@sinaihealth.ca'

`EPDS_FU_EMAIL`
    email address(es) of OBS staff who will follow-up with subjects who have EPDS issues. ::

        EPDS_FU_EMAIL = 'ryan.seeto@sinaihealth.ca; ryan.seeto@sinaihealth.ca'

`SENT_FROM_EMAIL`
    email address of individual who is sending the emails ::

        SENT_FROM_EMAIL = 'ryan.seeto@sinaihealth.ca'

`SENT_ON_BEHALF`
    email address of the 'Sent on behalf of' ::

        SENT_ON_BEHALF = 'OntarioBirthStudy.msh@sinaihealth.ca'

`OBS_OUTLOOK_FOLDER`
    OBS communal folder name ::

        OBS_OUTLOOK_FOLDER = 'Ontario Birth Study (MSH)'

`LSQ_GIVEN_GA`
    sets the gestational threshold for when associated LSQ is sent (e.g. when `lsq1ga` : (11*7), LSQ1 will be sent after 11 weeks). ::

        LSQ_GIVEN_GA = {
            'lsq1ga': (11*7),
            'lsq2ga': (26*7),
            'lsq3ga': (46*7),
            'lsq3dd': (6*7)
        }

`LSQ_FU_DAYS`
    sets the number of days after which a follow-up/reminder email will be sent ::

        LSQ_FU_DAYS = (2*7)

`CONTACT_PATH`
    path to the contact list; must be forward slash ::

        CONTACT_PATH = (
            'T:/Dept ObGyn Research/Ontario Birth Study/'
            'Patient contact information/Patient contact information.xlsx'
        )

`LINK_PATH`
    path to file with LSQ links and emails; must be forward slash ::

        LINK_PATH = (
            "T:/Dept ObGyn Research/Ontario Birth Study/Lifestyle Questionnaires/"
            "Distribution Passwords Emails/LSQpasswords.csv"
        )

`ACCESS_PATH`
    path to access database; must be backward slash ::

        ACCESS_PATH = r'T:\Dept ObGyn Research\Screening\Research Database.accdb'

`EMAIL_INFO`
    email information to be included in the LSQ emails ::

        EMAIL_INFO = {
            'LSQ(1)Given': {
                'link_subject': ('Ontario Birth Study Lifestyle Questionnaire 1'),
                'link_body':  (
                    "Dear Ontario Birth Study participant:\n\nThank you for enrolling"
                    " in the Ontario Birth Study. As part of the study, you will be"
                    " asked to complete 3 Lifestyle Questionnaires and 1 Diet History"
                    " Questionnaire. These questionnaires are designed to improve"
                    " our understanding of mother's and infant's health during"
                    " pregnancy and how this influences health over the life"
                    " course.\nA link to Lifestyle Questionnaire 1 is below:\n\n"
                    "{}"  # link place holder
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nYou will receive Lifestyle Questionnaire"
                    " 2 when you are approximately 28 weeks gestational age. If you"
                    " have any questions, feel free to contact the Ontario Birth"
                    " Study at ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext."
                    " 6036. Once again, thank you for participating in the Ontario"
                    " Birth Study. Without your help, this research would not be"
                    " possible.\n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Password'
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(1)Followup1': {
                'link_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 1 Follow-up"
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 1 is"
                    " below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nIf you have any questions, feel free to"
                    " contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Password'
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(1)Followup2': {
                'link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Follow-up'
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 1 is"
                    " below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nIf you would like a paper copy of the"
                    " Lifestyle Questionnaire or if you have any questions, feel free"
                    " to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 1 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(1)Followup3': {
                'link_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 1 Follow-up"
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 1 is"
                    " below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nIf you would like a paper copy of the"
                    " Lifestyle Questionnaire or if you have any questions,"
                    " feel free to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 1 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(2)Given': {
                'link_subject': ("Ontario Birth Study Lifestyle Questionnaire 2"),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nIncluded below is a"
                    " link to the Ontario Birth Study Lifestyle Questionnaire 2:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 2. \n\nYou will receive Lifestyle Questionnaire 3"
                    " when you are approximately 6 weeks postpartum. If you have any"
                    " questions, feel free to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nOnce again, thank you for participating in the Ontario"
                    " Birth Study. Without your help, this research would not be"
                    " possible.\n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 2 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 2 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(2)Followup1': {
                'link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 2 Follow-up'
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 2 is"
                    " below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 2. \n\nIf you have any questions, feel free to"
                    " contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 2 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 2 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(2)Followup2': {
                'link_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 2 Follow-up"
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 2 is"
                    " below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 2. \n\nIf you would like a paper copy of the"
                    " Lifestyle Questionnaire or if you have any questions, feel free"
                    " to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 2 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 2 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(2)Followup3': {
                'link_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 2 Follow-up"
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 2"
                    " is below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 2. \n\nIf you would like a paper copy of the"
                    " Lifestyle Questionnaire or if you have any questions, feel"
                    " free to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 2 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 2 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(3)Given': {
                'link_subject': ("Ontario Birth Study Lifestyle Questionnaire 3"),
                'link_body': (
                    "Dear Ontario Birth Study participant: \n\nCongratulations on"
                    " your new baby! This is the last survey for the Ontario Birth"
                    " Study. Once you complete this survey, you have fulfilled your"
                    " obligations to this study. A link to the Lifestyle"
                    " Questionnaire 3 is below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 3. \n\nIf you have any questions, feel free to"
                    " contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nOnce again, thank you for participating in the Ontario"
                    " Birth Study. Without your help, this research would not be"
                    " possible.\n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 3 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 3 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(3)Followup1': {
                'link_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 3 Follow-up"
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 3 is"
                    " below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 3. \n\nIf you have any questions, feel free to"
                    " contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 3 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 3 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(3)Followup2': {
                'link_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 3 Follow-up"
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 3 is"
                    " below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 3. \n\nIf you would like a paper copy of the"
                    " Lifestyle Questionnaire or if you have any questions, feel free"
                    " to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 3 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 3 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },

            'LSQ(3)Followup3': {
                'link_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 3 Follow-up"
                ),
                'link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 3 is"
                    " below:\n\n"
                    "{}"
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 3. \n\nIf you would like a paper copy of the"
                    " Lifestyle Questionnaire or if you have any questions, feel free"
                    " to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                ),
                'password_subject': (
                    "Ontario Birth Study Lifestyle Questionnaire 3 Password"
                ),
                'password_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 3 is as follows:\n\n"
                    "{}"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },
        }



In addition, a file called `obs_email_lsq/obs_email_lsq/config_api.py` will need to be created. This file should contain a dictionary with the APIs of the associated LSQs. The API information should be available from the current institution hosting the REDCap instance. At the time of writing, the OBS LSQs were hosted at the `Applied Health Research Centre <https://www.hubresearch.ca/>`_. An example of the `config_api.py` is below::

    redcap_api = {
        'lsq1': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'lsq2': 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
        'lsq3': 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC'   
    }