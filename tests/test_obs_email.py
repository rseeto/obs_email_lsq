"""Tests for obs_email module"""

import datetime
import pandas as pd
import obs_email
import pytest
import numpy as np
from _pytest.monkeypatch import monkeypatch
import pyodbc

def test_ObsParticipants_set_access_table():
    """Test obs_email.ObsParticipants.set_access_table"""
    actual = obs_email.ObsParticipants()

    ref_enrolment = pd.DataFrame(# enrolment
        {
            'obs_study_id': [91200001, 91200002, 91200003],
            'EDC' : ['2020-01-01', '2000-01-01', '2019-01-01'],
            'DIPLateEntry': [True, True, True],
            'DIPCurEnrol': [True, True, True]
        }
    )

    ref_followup = pd.DataFrame(# followup
        {
            'obs_study_id': [91200001, 91200002, 91200003],
            'PatientID': ['.01', '.02', '.03'],
            'PatientFirstName': ['FN1', 'FN2', 'FN3'],
            'PatientSurname': ['SN1', 'SN2', 'SN3'],
            'col1': ['No', 'No', 'Yes']
        }
    )
    actual.set_access_table(ref_enrolment, ref_followup)
    actual.access_table.reset_index(drop=True, inplace=True)

    expected_id_enrol = ['91200001', '91200003']
    assert actual.id_enrol == expected_id_enrol

    expected_access_patient_info = { # expected_access_patient_info
        '91200001': {
            'PatientID': '1',
            'PatientFirstName': 'FN1',
            'PatientSurname': 'SN1'
        },
        '91200003': {
            'PatientID': '3',
            'PatientFirstName': 'FN3',
            'PatientSurname': 'SN3'
        }
    }
    assert actual.access_patient_info == expected_access_patient_info

    expected_access_table = pd.DataFrame(# expected_access_table
        {
            'obs_study_id': ['91200001', '91200003'],
            'EDC' : [
                datetime.date(year=2020, month=1, day=1),
                datetime.date(year=2019, month=1, day=1)
            ],
            'DIPLateEntry': [True, True],
            'DIPCurEnrol': [True, True],
            'PatientID': ['1', '3'],
            'PatientFirstName': ['FN1', 'FN3'],
            'PatientSurname': ['SN1', 'SN3'],
            'col1': ['No', 'Yes'],
            'LMP': [
                datetime.date(year=2019, month=3, day=27),
                datetime.date(year=2018, month=3, day=27)
            ]
        }
    )
    for col_name in actual.access_table.columns.values.tolist():
        assert all(
            actual.access_table[col_name] == (
                expected_access_table[col_name]
            )
        )

def test_ObsParticipants_remove_exclusion_ids():
    """Test obs_email.ObsParticipants.remove_exclusion_ids"""
    actual_df = pd.DataFrame(# expected_access_table
        {'obs_study_id': ['91200001', '91200002', '91200003', '91200004']}
    )
    obs_email.ObsParticipants.access_table = actual_df
    obs_email.ObsParticipants.id_enrol = list(actual_df['obs_study_id'])

    obs_email.ObsParticipants.remove_exclusion_ids([91200002, 91200004])

    expected_df = pd.DataFrame(# expected_access_table
        {'obs_study_id': ['91200001', '91200003']}
    )

    assert obs_email.ObsParticipants.id_excl == [91200002, 91200004]
    assert expected_df.equals(
        obs_email.ObsParticipants.access_wo_excl.reset_index(drop=True)
    )

def test_ObsParticipants_set_emails_link_pwd():
    """Test obs_email.ObsParticipants.set_emails_link_pwd"""
    obs_email.ObsParticipants.id_excl = [91200002]
    obs_email.ObsParticipants.set_emails_link_pwd(
        'tests/data/Patient contact information.xlsx',
        'tests/data/LSQpasswords.csv'
    )

    expected_emails_link_pwd_dict = {
        '91200001':{
            'E-mail': 'fake_email_1@gmail.com',
            'lsq1_password': 'lsq1pss1',
            'lsq1_website': 'https://redcap.smh.ca/redcap/surveys/?s=11111AAAAA',
            'lsq2_password': 'lsq2pss1',
            'lsq2_website': 'https://redcap.smh.ca/redcap/surveys/?s=11111AAAAA',
            'lsq3_password': 'lsq3pss1',
            'lsq3_website': 'https://redcap.smh.ca/redcap/surveys/?s=11111AAAAA'
        },
        '91200003':{
            'E-mail': 'fake_email_3@gmail.com',
            'lsq1_password': 'lsq1pss3',
            'lsq1_website': 'https://redcap.smh.ca/redcap/surveys/?s=11111AAAAA',
            'lsq2_password': 'lsq2pss3',
            'lsq2_website': 'https://redcap.smh.ca/redcap/surveys/?s=11111AAAAA',
            'lsq3_password': 'lsq3pss3',
            'lsq3_website': 'https://redcap.smh.ca/redcap/surveys/?s=11111AAAAA'
        },
    }

    assert (
        obs_email.ObsParticipants.emails_link_pwd_dict == (
            expected_emails_link_pwd_dict
        )
    )

param_Lsq_init = [
    (# single subject given and returned, already documented
        pd.DataFrame(# enrolment
            {
                'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                'EDC' : ['2020-01-01', '2020-01-01', '2020-01-01', '2020-01-01'],
                'DIPLateEntry': [True, True, True, True],
                'DIPCurEnrol': [True, True, True, True]
            }
        ),
        pd.DataFrame(# followup
            {
                'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                'PatientID': ['.01', '.02', '.03', '.04'],
                'PatientFirstName': ['FN1', 'FN2', 'FN3', 'FN4'],
                'PatientSurname': ['SN1', 'SN2', 'SN3', 'FN4'],
                'LSQ(1)Given' : [True, False, False, False],
                'LSQ(1)Returned': [True, False, False, False]
            }
        ),
        '1', # lsq_num
        pd.DataFrame( # redcap_lsq
            {
                'obs_study_id': [91200001],
                'lifestyle_questionnaire_1_timestamp': [
                    '2019-01-01 00:00:01'
                ],
                'superflous_column': ['A']
            }
        ),
        '1', # expected_lsq_num
        [], # expected_id_access_not_returned
        pd.DataFrame( # expected_redcap_lsq_comp
            {
                'obs_study_id': [91200001],
                'lifestyle_questionnaire_1_timestamp': ['2019-01-01']
            }
        )
    ),
    (# single subject not returned

        pd.DataFrame(# enrolment
            {
                'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                'EDC' : ['2020-01-01', '2020-01-01', '2020-01-01', '2020-01-01'],
                'DIPLateEntry': [True, True, True, True],
                'DIPCurEnrol': [True, True, True, True]
            }
        ),
        pd.DataFrame(# followup
            {
                'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                'PatientID': ['.01', '.02', '.03', '.04'],
                'PatientFirstName': ['FN1', 'FN2', 'FN3', 'FN4'],
                'PatientSurname': ['SN1', 'SN2', 'SN3', 'FN4'],
                'LSQ(1)Given' : [True, True, False, False],
                'LSQ(1)Returned': [True, False, False, False]
            }
        ),
        '1', # lsq_num
        pd.DataFrame( # redcap_lsq
            {
                'obs_study_id': [91200001],
                'lifestyle_questionnaire_1_timestamp': [
                    '2019-01-01 00:00:01'
                ],
                'superflous_column': ['A']
            }
        ),
        '1', # expected_lsq_num
        ['91200002'], # expected_id_access_not_returned
        pd.DataFrame( # expected_redcap_lsq_comp
            {
                'obs_study_id': [91200001],
                'lifestyle_questionnaire_1_timestamp': ['2019-01-01']
            }
        )
    ),
    (# combination of given and returned
        pd.DataFrame(# enrolment
            {
                'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                'EDC' : ['2020-01-01', '2020-01-01', '2020-01-01', '2020-01-01'],
                'DIPLateEntry': [True, True, True, True],
                'DIPCurEnrol': [True, True, True, True]
            }
        ),
        pd.DataFrame(# followup
            {
                'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                'PatientID': ['.01', '.02', '.03', '.04'],
                'PatientFirstName': ['FN1', 'FN2', 'FN3', 'FN4'],
                'PatientSurname': ['SN1', 'SN2', 'SN3', 'FN4'],
                'LSQ(1)Given' : [True, True, False, True],
                'LSQ(1)Returned': [True, False, False, False]
            }
        ),
        '1', # lsq_num
        pd.DataFrame( # redcap_lsq
            {
                'obs_study_id': [91200001, 91200002],
                'lifestyle_questionnaire_1_timestamp': [
                    '2019-01-01 00:00:01', '2020-01-30 23:59:59'
                ],
                'superflous_column': ['A', 'A']
            }
        ),
        '1', # expected_lsq_num
        ['91200002', '91200004'], # expected_id_access_not_returned
        pd.DataFrame( # expected_redcap_lsq_comp
            {
                'obs_study_id': [91200001, 91200002],
                'lifestyle_questionnaire_1_timestamp': ['2019-01-01', '2020-01-30']
            }
        )
    ),
]

@pytest.mark.parametrize(
    (
        'ref_enrolment_2, ref_followup_2, lsq_num_2, redcap_lsq_2, '
        'expected_lsq_num_2, expected_id_access_not_returned_2, '
        'expected_redcap_lsq_comp_2'
    ), param_Lsq_init
)

def test_Lsq_init(
    ref_enrolment_2, ref_followup_2, lsq_num_2, redcap_lsq_2,
    expected_lsq_num_2, expected_id_access_not_returned_2,
    expected_redcap_lsq_comp_2
):
    """Test obs_email.Lsq.__init__"""
    obs_email.ObsParticipants.set_access_table(ref_enrolment_2, ref_followup_2)

    actual_lsq_1 = obs_email.Lsq(lsq_num_2, redcap_lsq_2)

    assert actual_lsq_1.lsq_num == expected_lsq_num_2
    assert actual_lsq_1.id_access_not_returned == expected_id_access_not_returned_2
    for col_name in actual_lsq_1.redcap_lsq_comp.columns.values.tolist():
        assert all(
            actual_lsq_1.redcap_lsq_comp[col_name] == (
                expected_redcap_lsq_comp_2[col_name]
            )
        )

@pytest.fixture
def ObsParticipants_template():
    """Create obs_email.ObsParticipants template

    Function creates obs_email.ObsParticipants template which is intended to be
    imported into Lsq_template (template for obs_email.Lsq)
    """
    empty_enrolment = pd.DataFrame(# enrolment
        {'obs_study_id': [], 'EDC' : [], 'DIPLateEntry': [], 'DIPCurEnrol': []}
    )
    empty_followup = pd.DataFrame(# followup
        {
            'obs_study_id': [], 'PatientID': [], 'PatientFirstName': [],
            'PatientSurname': [],
            'LSQ(1)Given' : [], 'LSQ(1)Returned': [],
            'LSQ(2)Given' : [], 'LSQ(2)Returned': [],
            'LSQ(3)Given' : [], 'LSQ(3)Returned': []
        }
    )
    obs_email.ObsParticipants.set_access_table(empty_enrolment, empty_followup)
    obs_email.ObsParticipants.remove_exclusion_ids([])

    obs_email.ObsParticipants.set_emails_link_pwd(
        'tests/data/Patient contact information.xlsx',
        'tests/data/LSQpasswords.csv'
    )

    return obs_email.ObsParticipants

@pytest.fixture
def Lsq_template(ObsParticipants_template):
    """Create obs_email.Lsq template"""

    obs_email.ObsParticipants = ObsParticipants_template

    empty_redcap_lsq = pd.DataFrame(
        {
            'obs_study_id': [],
            'lifestyle_questionnaire_1_timestamp': [],
            'lifestyle_questionnaire_2_timestamp': [],
            'lifestyle_questionnaire_3_timestamp': []
        }
    )
    lsq_1 = obs_email.Lsq('1', empty_redcap_lsq)
    lsq_2 = obs_email.Lsq('2', empty_redcap_lsq)
    lsq_3 = obs_email.Lsq('3', empty_redcap_lsq)

    return lsq_1, lsq_2, lsq_3

param_Lsq_update_access_returned = [
    ( # single subject
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        pd.DataFrame( # redcap info
            {
                'obs_study_id': ['91200001', '91200002'],
                'lifestyle_questionnaire_1_timestamp': [
                    '2019-01-01', '2020-01-30'
                ]
            }
        ),
        ['91200001'], # id access not returned
        [
            {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Returned") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200001',
                'obs_access_id': '912-00001',
                'patient_first_name': 'PatientFirstName_91200001',
                'patient_surname': 'PatientSurname_91200001',
                'date_compl': '2019-01-01',
                'bool_val': 1
            }
        ]# expected_sql_commands_3
    ),
    ( # multiple subjects
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        pd.DataFrame( # redcap info
            {
                'obs_study_id': ['91200001', '91200002'],
                'lifestyle_questionnaire_1_timestamp': [
                    '2019-01-01', '2020-01-30'
                ]
            }
        ),
        ['91200001', '91200002'], # id access not returned
        [
            {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Returned") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200001',
                'obs_access_id': '912-00001',
                'patient_first_name': 'PatientFirstName_91200001',
                'patient_surname': 'PatientSurname_91200001',
                'date_compl': '2019-01-01',
                'bool_val': 1
            }, {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Returned") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200002',
                'obs_access_id': '912-00002',
                'patient_first_name': 'PatientFirstName_91200002',
                'patient_surname': 'PatientSurname_91200002',
                'date_compl': '2020-01-30',
                'bool_val': 1
            }
        ]# expected_sql_commands_3
    ),
    ( # zero subjects
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        pd.DataFrame( # redcap info
            {
                'obs_study_id': ['91200001', '91200002'],
                'lifestyle_questionnaire_1_timestamp': [
                    '2019-01-01', '2020-01-30'
                ]
            }
        ),
        [], # id access not returned
        [] # expected_sql_commands_3
    ),
]

@pytest.mark.parametrize(
    (
        'access_patient_info_3, redcap_lsq_comp_3, id_access_not_returned_3,'
        'expected_sql_commands_3'
    ),
    param_Lsq_update_access_returned
)

def test_Lsq_update_access_returned(
    access_patient_info_3, redcap_lsq_comp_3, id_access_not_returned_3,
    expected_sql_commands_3, Lsq_template, monkeypatch
):
    """Test obs_data.Lsq.update_access_returned

    Notes
    -----
    https://docs.pytest.org/en/6.2.x/
    monkeypatch.html#monkeypatching-returned-objects-building-mock-classes
    """

    lsq_1, _, _ = Lsq_template

    actual_sql_commands = []
    class MockPyodbcCursor:
        """Class to monkeypatch pyodbc.connect.cursor"""
        @staticmethod
        def execute(
            statement, patient_id, obs_access_id, patient_first_name,
            patient_surname, date_compl, bool_val
        ):
            """Method to monkeypatch pyodbc.connect.cursor.execute"""
            sql_syntax = {
                'statement': statement,
                'patient_id': patient_id,
                'obs_access_id': obs_access_id,
                'patient_first_name': patient_first_name,
                'patient_surname': patient_surname,
                'date_compl': date_compl,
                'bool_val': bool_val
            }
            actual_sql_commands.append(sql_syntax)

    class MockPyodbc:
        """Class to monkeypatch pyodbc.connect"""
        @staticmethod
        def cursor():
            """Method to monkeypatch pyodbc.connect.cursor"""
            return MockPyodbcCursor()
        @staticmethod
        def commit():
            """Method to monkeypatch pyodbc.connect.cursor.commit"""
            pass
        @staticmethod
        def close():
            """Method to monkeypatch pyodbc.connect.cursor.close"""
            pass

    def mock_connect(*args, **kwargs):
        return MockPyodbc()

    monkeypatch.setattr(pyodbc, 'connect', mock_connect)

    lsq_1.access_patient_info = access_patient_info_3
    lsq_1.redcap_lsq_comp = redcap_lsq_comp_3
    lsq_1.id_access_not_returned = id_access_not_returned_3
    lsq_1.update_access_returned('fake_testing_path')

    assert actual_sql_commands == expected_sql_commands_3

param_Lsq_set_lsq_status = [
    ( # no follow up due to insufficient days ('OBSVisitDate'), Given
        pd.DataFrame(# access_wo_excl
                {

                    'obs_study_id': [
                        '91200001', '91200002', '91200003', '91200004', '91200005'
                    ],
                    'LSQ(1)Returned' : [False, False, False, False, False],
                    'LSQ(1)Followup3': [False, False, False, False, False],
                    'LSQ1Refused': [False, False, False, False, False],
                    'Paper LSQ1': [False, False, False, False, False],
                    'LSQ(1)Given': [True, True, True, True, True],
                    'LSQ(1)Followup1': [False, False, False, False, False],
                    'LSQ(1)Followup2': [False, False, False, False, False],
                    'OBSVisitDate': [
                        datetime.date(year=2020, month=1, day=16),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=18),
                        datetime.date(year=2020, month=1, day=19),
                        datetime.date(year=2020, month=1, day=20)
                    ],
                    'LMP': [
                        datetime.date(year=2019, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27)
                    ],

                }
            ),
        pd.DataFrame({'obs_study_id': []}),
        ['91200003', '91200004', '91200005'],
        {
            'LSQ(1)Given': [],
            'LSQ(1)Followup1': ['91200001', '91200002'],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup3': []
        }
    ), ( # no follow up due to insufficient days ('OBSVisitDate'),
        # Followup 1
        pd.DataFrame(# access_wo_excl
                {

                    'obs_study_id': [
                        '91200001', '91200002', '91200003', '91200004', '91200005'
                    ],
                    'LSQ(1)Returned' : [False, False, False, False, False],
                    'LSQ(1)Followup3': [False, False, False, False, False],
                    'LSQ1Refused': [False, False, False, False, False],
                    'Paper LSQ1': [False, False, False, False, False],
                    'LSQ(1)Given': [False, False, False, False, False],
                    'LSQ(1)Followup1': [True, True, True, True, True],
                    'LSQ(1)Followup2': [False, False, False, False, False],
                    'OBSVisitDate': [
                        datetime.date(year=2020, month=1, day=16),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=18),
                        datetime.date(year=2020, month=1, day=19),
                        datetime.date(year=2020, month=1, day=20)
                    ],
                    'LMP': [
                        datetime.date(year=2019, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27)
                    ],

                }
            ),
        pd.DataFrame({'obs_study_id': []}),
        ['91200003', '91200004', '91200005'],
        {
            'LSQ(1)Given': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Followup2': ['91200001', '91200002'],
            'LSQ(1)Followup3': []
        }
    ), ( # no follow up due to insufficient days ('OBSVisitDate') passing,
        # Followup 2
        pd.DataFrame(# access_wo_excl
                {

                    'obs_study_id': [
                        '91200001', '91200002', '91200003', '91200004', '91200005'
                    ],
                    'LSQ(1)Returned' : [False, False, False, False, False],
                    'LSQ(1)Followup3': [False, False, False, False, False],
                    'LSQ1Refused': [False, False, False, False, False],
                    'Paper LSQ1': [False, False, False, False, False],
                    'LSQ(1)Given': [False, False, False, False, False],
                    'LSQ(1)Followup1': [False, False, False, False, False],
                    'LSQ(1)Followup2': [True, True, True, True, True],
                    'OBSVisitDate': [
                        datetime.date(year=2020, month=1, day=16),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=18),
                        datetime.date(year=2020, month=1, day=19),
                        datetime.date(year=2020, month=1, day=20)
                    ],
                    'LMP': [
                        datetime.date(year=2019, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27)
                    ],

                }
            ),
        pd.DataFrame({'obs_study_id': []}),
        ['91200003', '91200004', '91200005'],
        {
            'LSQ(1)Given': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup3': ['91200001', '91200002']
        }
    ), ( # no follow up due to completing LSQ
        pd.DataFrame(# access_wo_excl
                {

                    'obs_study_id': [
                        '91200001', '91200002', '91200003', '91200004', '91200005'
                    ],
                    'LSQ(1)Returned' : [False, False, False, False, False],
                    'LSQ(1)Followup3': [False, False, False, False, False],
                    'LSQ1Refused': [False, False, False, False, False],
                    'Paper LSQ1': [False, False, False, False, False],
                    'LSQ(1)Given': [True, True, True, True, True],
                    'LSQ(1)Followup1': [False, False, False, False, False],
                    'LSQ(1)Followup2': [False, False, False, False, False],
                    'OBSVisitDate': [
                        datetime.date(year=2020, month=1, day=16),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=18),
                        datetime.date(year=2020, month=1, day=19),
                        datetime.date(year=2020, month=1, day=20)
                    ],
                    'LMP': [
                        datetime.date(year=2019, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27)
                    ],

                }
            ),
        pd.DataFrame({'obs_study_id': ['91200001']}),
        ['91200001', '91200003', '91200004', '91200005'],
        {
            'LSQ(1)Given': [],
            'LSQ(1)Followup1': ['91200002'],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup3': []
        }
    ), ( # no follow up due to information in Access
        pd.DataFrame(# access_wo_excl
                {

                    'obs_study_id': [
                        '91200001', '91200002', '91200003', '91200004', '91200005'
                    ],
                    'LSQ(1)Returned' : [False, True, False, False, False],
                    'LSQ(1)Followup3': [False, False, True, False, False],
                    'LSQ1Refused': [False, False, False, True, False],
                    'Paper LSQ1': [False, False, False, False, True],
                    'LSQ(1)Given': [True, False, False, False, False],
                    'LSQ(1)Followup1': [False, False, False, False, False],
                    'LSQ(1)Followup2': [False, False, False, False, False],
                    'OBSVisitDate': [
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=17)
                    ],
                    'LMP': [
                        datetime.date(year=2019, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27),
                        datetime.date(year=2018, month=3, day=27)
                    ],

                }
            ),
        pd.DataFrame({'obs_study_id': []}),
        ['91200002', '91200003', '91200004', '91200005'],
        {
            'LSQ(1)Given': [],
            'LSQ(1)Followup1': ['91200001'],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup3': []
        }
    ),
    ( # LSQ(1)Given based on threshold date (set in config.py)
        pd.DataFrame(# access_wo_excl
                {
                    'obs_study_id': [
                        '91200001', '91200002', '91200003', '91200004', '91200005'
                    ],
                    'LSQ(1)Returned' : [False, False, False, False, False],
                    'LSQ(1)Followup3': [False, False, False, False, False],
                    'LSQ1Refused': [False, False, False, False, False],
                    'Paper LSQ1': [False, False, False, False, False],
                    'LSQ(1)Given': [False, False, False, False, False],
                    'LSQ(1)Followup1': [False, False, False, False, False],
                    'LSQ(1)Followup2': [False, False, False, False, False],
                    'OBSVisitDate': [
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=17),
                        datetime.date(year=2020, month=1, day=17)
                    ],
                    'LMP': [
                        datetime.date(year=2019, month=11, day=13),
                        datetime.date(year=2019, month=11, day=14),
                        datetime.date(year=2019, month=11, day=15),
                        datetime.date(year=2019, month=11, day=16),
                        datetime.date(year=2019, month=11, day=17)
                    ],

                }
            ),
        pd.DataFrame({'obs_study_id': []}),
        [],
        {
            'LSQ(1)Given': ['91200001', '91200002', '91200003'],
            'LSQ(1)Followup1': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup3': []
        }
    ),
]

@pytest.mark.parametrize(
    'access_wo_excl_4, redcap_lsq_comp_4, expected_lsq_no_fu_4, expected_lsq_status_4',
    param_Lsq_set_lsq_status
)

def test_Lsq_set_lsq_status(
    access_wo_excl_4, redcap_lsq_comp_4, expected_lsq_no_fu_4,
    expected_lsq_status_4,
    Lsq_template, monkeypatch
):
    """Test obs_data.Lsq.set_lsq_status"""
    lsq_1, _, _ = Lsq_template
    lsq_1.access_wo_excl = access_wo_excl_4
    lsq_1.redcap_lsq_comp = redcap_lsq_comp_4

    class MockPdTimestamp:
        """Class to monkeypatch pd.Timestamp"""
        @classmethod
        def today(cls):
            """Method to monkeypatch pd.Timestamp.today"""
            mock_today = np.datetime64('2020-01-31')
            return mock_today
    monkeypatch.setattr(pd, 'Timestamp', MockPdTimestamp)

    lsq_1.set_lsq_status()

    assert(set(lsq_1._lsq_no_fu) == set(expected_lsq_no_fu_4))
    for key in expected_lsq_status_4.keys():
        assert(set(lsq_1.lsq_status[key]) == set(expected_lsq_status_4[key]))

param_Lsq_remove_lsq_priority = [
    ( # doc string example
        [], #followup3
        ['1'], #followup2
        ['2'], #followup1
        ['3'], #given
        ['1', '2'], #remove_ids
        [], #expected_followup3
        [], #expected_followup2
        [], #expected_followup1
        ['3'] #expected_given
    ),
    ( # remove ids from followup3
        ['1', '2'], #followup3
        [], #followup2
        [], #followup1
        [], #given
        ['1'], #remove_ids
        ['2'], #expected_followup3
        [], #expected_followup2
        [], #expected_followup1
        [] #expected_given
    ),
    ( # remove ids from followup2
        [], #followup3
        ['1', '2'], #followup2
        [], #followup1
        [], #given
        ['1'], #remove_ids
        [], #expected_followup3
        ['2'], #expected_followup2
        [], #expected_followup1
        [] #expected_given
    ),
    ( # remove ids from followup1
        [], #followup3
        [], #followup2
        ['1', '2'], #followup1
        [], #given
        ['1'], #remove_ids
        [], #expected_followup3
        [], #expected_followup2
        ['2'], #expected_followup1
        [] #expected_given
    ),
    ( # remove ids from given
        [], #followup3
        [], #followup2
        [], #followup1
        ['1', '2'], #given
        ['1'], #remove_ids
        [], #expected_followup3
        [], #expected_followup2
        [], #expected_followup1
        ['2'] #expected_given
    ),
    ( # no ids to remove
        ['4'], #followup3
        ['3'], #followup2
        ['2'], #followup1
        ['1'], #given
        [], #remove_ids
        ['4'], #expected_followup3
        ['3'], #expected_followup2
        ['2'], #expected_followup1
        ['1'] #expected_given
    ),
]

@pytest.mark.parametrize(
    (
        'followup3, followup2, followup1, given, remove_ids,'
        'expected_followup3, expected_followup2, expected_followup1,'
        'expected_given'
    ),
    param_Lsq_remove_lsq_priority
)

def test_Lsq_remove_lsq_priority(
    followup3, followup2, followup1, given, remove_ids,
    expected_followup3, expected_followup2, expected_followup1,
    expected_given, Lsq_template
):
    """Test obs_data.Lsq.remove_lsq_priority"""
    lsq_1, _, _ = Lsq_template

    lsq_1.lsq_status = {}
    lsq_1.lsq_status['LSQ(1)Followup3'] = followup3
    lsq_1.lsq_status['LSQ(1)Followup2'] = followup2
    lsq_1.lsq_status['LSQ(1)Followup1'] = followup1
    lsq_1.lsq_status['LSQ(1)Given'] = given

    lsq_1.remove_lsq_priority(remove_ids)

    assert lsq_1.lsq_status['LSQ(1)Followup3'] == expected_followup3
    assert lsq_1.lsq_status['LSQ(1)Followup2'] == expected_followup2
    assert lsq_1.lsq_status['LSQ(1)Followup1'] == expected_followup1
    assert lsq_1.lsq_status['LSQ(1)Given'] == expected_given

param_Lsq_send_lsq_emails = [
    ( # one subject, given status
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': ['91200001']
        },
        {#expected_emails_link_pwd_dict
            '91200001':{
                'E-mail': 'fake_email_1@gmail.com',
                'lsq1_password': 'lsq1pss1',
                'lsq1_website': 'https://lsq1website.ca/91200001',
                'lsq2_password': 'lsq2pss1',
                'lsq2_website': 'https://lsq2website.ca/91200001',
                'lsq3_password': 'lsq3pss1',
                'lsq3_website': 'https://lsq3website.ca/91200001'
            },
            '91200002':{
                'E-mail': 'fake_email_2@gmail.com',
                'lsq1_password': 'lsq1pss2',
                'lsq1_website': 'https://lsq1website.ca/91200002',
                'lsq2_password': 'lsq2pss2',
                'lsq2_website': 'https://lsq2website.ca/91200002',
                'lsq3_password': 'lsq3pss2',
                'lsq3_website': 'https://lsq3website.ca/91200003'
            },
        },
        [ # expected_send_email
            {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nThank you for enrolling"
                    " in the Ontario Birth Study. As part of the study, you will be"
                    " asked to complete 3 Lifestyle Questionnaires and 1 Diet History"
                    " Questionnaire. These questionnaires are designed to improve"
                    " our understanding of mother's and infant's health during"
                    " pregnancy and how this influences health over the life"
                    " course.\nA link to Lifestyle Questionnaire 1 is below:\n\n"
                    "https://lsq1website.ca/91200001"  # link place holder
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nYou will receive Lifestyle Questionnaire"
                    " 2 when you are approximately 28 weeks gestational age. If you"
                    " have any questions, feel free to contact the Ontario Birth"
                    " Study at ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext."
                    " 6036. Once again, thank you for participating in the Ontario"
                    " Birth Study. Without your help, this research would not be"
                    " possible.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            }, {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Password'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "lsq1pss1"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },
        ]
    ),
    ( # one subject, follow up 1
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': ['91200001'],
            'LSQ(1)Given': []
        },
        {#expected_emails_link_pwd_dict
            '91200001':{
                'E-mail': 'fake_email_1@gmail.com',
                'lsq1_password': 'lsq1pss1',
                'lsq1_website': 'https://lsq1website.ca/91200001',
                'lsq2_password': 'lsq2pss1',
                'lsq2_website': 'https://lsq2website.ca/91200001',
                'lsq3_password': 'lsq3pss1',
                'lsq3_website': 'https://lsq3website.ca/91200001'
            },
            '91200002':{
                'E-mail': 'fake_email_2@gmail.com',
                'lsq1_password': 'lsq1pss2',
                'lsq1_website': 'https://lsq1website.ca/91200002',
                'lsq2_password': 'lsq2pss2',
                'lsq2_website': 'https://lsq2website.ca/91200002',
                'lsq3_password': 'lsq3pss2',
                'lsq3_website': 'https://lsq3website.ca/91200003'
            },
        },
        [ # expected_send_email
            {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Follow-up'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 1 is"
                    " below:\n\n"
                    "https://lsq1website.ca/91200001"  # link place holder
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nIf you have any questions, feel free to"
                    " contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            }, {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Password'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "lsq1pss1"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },
        ]
    ),
    ( # one subject, follow up 2
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': ['91200001'],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': []
        },
        {#expected_emails_link_pwd_dict
            '91200001':{
                'E-mail': 'fake_email_1@gmail.com',
                'lsq1_password': 'lsq1pss1',
                'lsq1_website': 'https://lsq1website.ca/91200001',
                'lsq2_password': 'lsq2pss1',
                'lsq2_website': 'https://lsq2website.ca/91200001',
                'lsq3_password': 'lsq3pss1',
                'lsq3_website': 'https://lsq3website.ca/91200001'
            },
            '91200002':{
                'E-mail': 'fake_email_2@gmail.com',
                'lsq1_password': 'lsq1pss2',
                'lsq1_website': 'https://lsq1website.ca/91200002',
                'lsq2_password': 'lsq2pss2',
                'lsq2_website': 'https://lsq2website.ca/91200002',
                'lsq3_password': 'lsq3pss2',
                'lsq3_website': 'https://lsq3website.ca/91200003'
            },
        },
        [ # expected_send_email
            {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Follow-up'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 1 is"
                    " below:\n\n"
                    "https://lsq1website.ca/91200001"  # link place holder
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nIf you would like a paper copy of the"
                    " Lifestyle Questionnaire or if you have any questions, feel free"
                    " to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            }, {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Password'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "lsq1pss1"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },
        ]
    ),
    ( # one subject, follow up 3
        { # lsq status
            'LSQ(1)Followup3': ['91200001'],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': []
        },
        {#expected_emails_link_pwd_dict
            '91200001':{
                'E-mail': 'fake_email_1@gmail.com',
                'lsq1_password': 'lsq1pss1',
                'lsq1_website': 'https://lsq1website.ca/91200001',
                'lsq2_password': 'lsq2pss1',
                'lsq2_website': 'https://lsq2website.ca/91200001',
                'lsq3_password': 'lsq3pss1',
                'lsq3_website': 'https://lsq3website.ca/91200001'
            },
            '91200002':{
                'E-mail': 'fake_email_2@gmail.com',
                'lsq1_password': 'lsq1pss2',
                'lsq1_website': 'https://lsq1website.ca/91200002',
                'lsq2_password': 'lsq2pss2',
                'lsq2_website': 'https://lsq2website.ca/91200002',
                'lsq3_password': 'lsq3pss2',
                'lsq3_website': 'https://lsq3website.ca/91200003'
            },
        },
        [ # expected_send_email
            {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Follow-up'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nThis is just a reminder"
                    " that you have not completed your most recent Lifestyle"
                    " Questionnaire.\n\nA link to Lifestyle Questionnaire 1 is"
                    " below:\n\n"
                    "https://lsq1website.ca/91200001"  # link place holder
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nIf you would like a paper copy of the"
                    " Lifestyle Questionnaire or if you have any questions,"
                    " feel free to contact the Ontario Birth Study at"
                    " ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext. 6036."
                    " \n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            }, {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Password'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "lsq1pss1"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },
        ]
    ),
    ( # no subjects
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': []
        },
        {#expected_emails_link_pwd_dict
            '91200001':{
                'E-mail': 'fake_email_1@gmail.com',
                'lsq1_password': 'lsq1pss1',
                'lsq1_website': 'https://lsq1website.ca/91200001',
                'lsq2_password': 'lsq2pss1',
                'lsq2_website': 'https://lsq2website.ca/91200001',
                'lsq3_password': 'lsq3pss1',
                'lsq3_website': 'https://lsq3website.ca/91200001'
            },
            '91200002':{
                'E-mail': 'fake_email_2@gmail.com',
                'lsq1_password': 'lsq1pss2',
                'lsq1_website': 'https://lsq1website.ca/91200002',
                'lsq2_password': 'lsq2pss2',
                'lsq2_website': 'https://lsq2website.ca/91200002',
                'lsq3_password': 'lsq3pss2',
                'lsq3_website': 'https://lsq3website.ca/91200003'
            },
        },
        [] # expected_send_email
    ),
    ( # multiple subjects
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': ['91200001', '91200002']
        },
        {#expected_emails_link_pwd_dict
            '91200001':{
                'E-mail': 'fake_email_1@gmail.com',
                'lsq1_password': 'lsq1pss1',
                'lsq1_website': 'https://lsq1website.ca/91200001',
                'lsq2_password': 'lsq2pss1',
                'lsq2_website': 'https://lsq2website.ca/91200001',
                'lsq3_password': 'lsq3pss1',
                'lsq3_website': 'https://lsq3website.ca/91200001'
            },
            '91200002':{
                'E-mail': 'fake_email_2@gmail.com',
                'lsq1_password': 'lsq1pss2',
                'lsq1_website': 'https://lsq1website.ca/91200002',
                'lsq2_password': 'lsq2pss2',
                'lsq2_website': 'https://lsq2website.ca/91200002',
                'lsq3_password': 'lsq3pss2',
                'lsq3_website': 'https://lsq3website.ca/91200003'
            },
        },
        [ # expected_send_email
            {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nThank you for enrolling"
                    " in the Ontario Birth Study. As part of the study, you will be"
                    " asked to complete 3 Lifestyle Questionnaires and 1 Diet History"
                    " Questionnaire. These questionnaires are designed to improve"
                    " our understanding of mother's and infant's health during"
                    " pregnancy and how this influences health over the life"
                    " course.\nA link to Lifestyle Questionnaire 1 is below:\n\n"
                    "https://lsq1website.ca/91200001"  # link place holder
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nYou will receive Lifestyle Questionnaire"
                    " 2 when you are approximately 28 weeks gestational age. If you"
                    " have any questions, feel free to contact the Ontario Birth"
                    " Study at ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext."
                    " 6036. Once again, thank you for participating in the Ontario"
                    " Birth Study. Without your help, this research would not be"
                    " possible.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            }, {
                'email_address': 'fake_email_1@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Password'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "lsq1pss1"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },
            {
                'email_address': 'fake_email_2@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nThank you for enrolling"
                    " in the Ontario Birth Study. As part of the study, you will be"
                    " asked to complete 3 Lifestyle Questionnaires and 1 Diet History"
                    " Questionnaire. These questionnaires are designed to improve"
                    " our understanding of mother's and infant's health during"
                    " pregnancy and how this influences health over the life"
                    " course.\nA link to Lifestyle Questionnaire 1 is below:\n\n"
                    "https://lsq1website.ca/91200002"  # link place holder
                    " \n\nA separate email will be sent to this email address which"
                    " contains a password to access your personal Lifestyle"
                    " Questionnaire 1. \n\nYou will receive Lifestyle Questionnaire"
                    " 2 when you are approximately 28 weeks gestational age. If you"
                    " have any questions, feel free to contact the Ontario Birth"
                    " Study at ontariobirthstudy@mtsinai.on.ca or 416-586-4800 ext."
                    " 6036. Once again, thank you for participating in the Ontario"
                    " Birth Study. Without your help, this research would not be"
                    " possible.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            }, {
                'email_address': 'fake_email_2@gmail.com',
                'lsq_link_subject': (
                    'Ontario Birth Study Lifestyle Questionnaire 1 Password'
                ),
                'lsq_link_body': (
                    "Dear Ontario Birth Study participant:\n\nYour password for"
                    " Lifestyle Questionnaire 1 is as follows:\n\n"
                    "lsq1pss2"
                    " \n\nPlease click the link provided in the previous email and"
                    " enter the above password to access your personal Lifestyle"
                    " Questionnaire.\n\nSincerely,\n\nThe Ontario Birth Study team"
                )
            },
        ]
    ),
]

@pytest.mark.parametrize(
    ('lsq_status_5, emails_link_pwd_dict_5, expected_send_email_5'),
    param_Lsq_send_lsq_emails
)

def test_Lsq_send_lsq_emails(
    lsq_status_5, emails_link_pwd_dict_5, expected_send_email_5,
    Lsq_template, monkeypatch
):
    """Test obs_email.Lsq.send_lsq_emails"""
    lsq_1, _, _ = Lsq_template
    lsq_1.lsq_status = lsq_status_5
    lsq_1.emails_link_pwd_dict = emails_link_pwd_dict_5

    actual_send_email = []
    def mock_send_email(email_address, lsq_link_subject, lsq_link_body):
        fun_args = {
                'email_address': email_address,
                'lsq_link_subject': lsq_link_subject,
                'lsq_link_body': lsq_link_body
        }
        actual_send_email.append(fun_args)
    monkeypatch.setattr(obs_email, 'send_email', mock_send_email)

    lsq_1.send_lsq_emails()

    assert actual_send_email == expected_send_email_5

param_Lsq_update_access_status = [
    ( # single subject, LSQ 1 given
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': ['91200001']
        },
        [
            {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Given") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200001',
                'obs_access_id': '912-00001',
                'patient_first_name': 'PatientFirstName_91200001',
                'patient_surname': 'PatientSurname_91200001',
                'date_compl': '2020-01-31',
                'bool_val': 1
            }
        ]# expected_sql_commands_5
    ),
    ( # single subject, LSQ 1 follow up 1
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': ['91200001'],
            'LSQ(1)Given': []
        },
        [
            {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Followup1") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200001',
                'obs_access_id': '912-00001',
                'patient_first_name': 'PatientFirstName_91200001',
                'patient_surname': 'PatientSurname_91200001',
                'date_compl': '2020-01-31',
                'bool_val': 1
            }
        ]# expected_sql_commands_5
    ),
    ( # single subject, LSQ 1 follow up 2
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': ['91200001'],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': []
        },
        [
            {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Followup2") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200001',
                'obs_access_id': '912-00001',
                'patient_first_name': 'PatientFirstName_91200001',
                'patient_surname': 'PatientSurname_91200001',
                'date_compl': '2020-01-31',
                'bool_val': 1
            }
        ]# expected_sql_commands_5
    ),
    ( # single subject, LSQ 1 follow up 3
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        { # lsq status
            'LSQ(1)Followup3': ['91200001'],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': []
        },
        [
            {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Followup3") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200001',
                'obs_access_id': '912-00001',
                'patient_first_name': 'PatientFirstName_91200001',
                'patient_surname': 'PatientSurname_91200001',
                'date_compl': '2020-01-31',
                'bool_val': 1
            }
        ]# expected_sql_commands_5
    ),
    ( # multiple subjects
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': ['91200001', '91200002']
        },
        [
            {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Given") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200001',
                'obs_access_id': '912-00001',
                'patient_first_name': 'PatientFirstName_91200001',
                'patient_surname': 'PatientSurname_91200001',
                'date_compl': '2020-01-31',
                'bool_val': 1
            },
            {
                'statement': (
                    'INSERT INTO OBSFollowupLog (PatientID, OBSEnrolmentID, '
                    'PatientFirstName, PatientSurname, OBSVisitDate, '
                    '"LSQ(1)Given") VALUES (?, ?, ?, ?, ?, ?)'
                ),
                'patient_id': 'PatientID_91200002',
                'obs_access_id': '912-00002',
                'patient_first_name': 'PatientFirstName_91200002',
                'patient_surname': 'PatientSurname_91200002',
                'date_compl': '2020-01-31',
                'bool_val': 1
            }
        ]# expected_sql_commands_5
    ),
    ( # no subjects
        {# access patient info
            '91200001': {# actual obs number
                'PatientID': 'PatientID_91200001',
                'PatientFirstName': 'PatientFirstName_91200001',
                'PatientSurname': 'PatientSurname_91200001'
            },
            '91200002': {# actual obs number
                'PatientID': 'PatientID_91200002',
                'PatientFirstName': 'PatientFirstName_91200002',
                'PatientSurname': 'PatientSurname_91200002'
            }
        },
        { # lsq status
            'LSQ(1)Followup3': [],
            'LSQ(1)Followup2': [],
            'LSQ(1)Followup1': [],
            'LSQ(1)Given': []
        },
        []# expected_sql_commands_5
    ),

]

@pytest.mark.parametrize(
    'access_patient_info_6, lsq_status_6, expected_sql_commands_6',
    param_Lsq_update_access_status
)

def test_Lsq_update_access_status(
    access_patient_info_6, lsq_status_6, expected_sql_commands_6,
    Lsq_template, monkeypatch
):
    """Test obs_data.Lsq.update_access_status"""
    lsq_1, _, _ = Lsq_template

    actual_sql_commands = []
    class MockPyodbcCursor:
        """Class to monkeypatch pyodbc.connect.cursor"""
        @staticmethod
        def execute(
            statement, patient_id, obs_access_id, patient_first_name,
            patient_surname, date_compl, bool_val
        ):
            """Method to monkeypatch pyodbc.connect.cursor.execute"""
            sql_syntax = {
                'statement': statement,
                'patient_id': patient_id,
                'obs_access_id': obs_access_id,
                'patient_first_name': patient_first_name,
                'patient_surname': patient_surname,
                'date_compl': date_compl,
                'bool_val': bool_val
            }
            actual_sql_commands.append(sql_syntax)
    class MockPyodbc:
        """Class to monkeypatch pyodbc.connect"""
        @staticmethod
        def cursor():
            """Method to monkeypatch pyodbc.connect.cursor"""
            return MockPyodbcCursor()
        @staticmethod
        def commit():
            """Method to monkeypatch pyodbc.connect.cursor.commit"""
            pass
        @staticmethod
        def close():
            """Method to monkeypatch pyodbc.connect.cursor.close"""
            pass
    def mock_connect(*args, **kwargs):
        return MockPyodbc()
    monkeypatch.setattr(pyodbc, 'connect', mock_connect)

    class NewDate(datetime.date):
        """Class to mock datetime.date

        Notes
        -----
        Can't mock date time directly since it's a built-in type, hence immutable
        https://stackoverflow.com/questions/4481954/
        trying-to-mock-datetime-date-today-but-not-working
        """

        @classmethod
        def today(cls):
            return cls(2020, 1, 31)
    datetime.date = NewDate

    lsq_1.access_patient_info = access_patient_info_6
    lsq_1.lsq_status = lsq_status_6
    lsq_1.update_access_status('fake_testing_path')

    print(actual_sql_commands)
    print(expected_sql_commands_6)

    assert actual_sql_commands == expected_sql_commands_6
