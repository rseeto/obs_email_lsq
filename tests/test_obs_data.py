"""Tests for obs_data module"""

import obs_data
import pandas as pd
import numpy as np
import pytest

def test_clean_access_table():
    """Test obs_data.clean_access_table"""
    actual = pd.DataFrame(
        {'OBSEnrolmentID': ['OBS912-00001', 'OBS912-00002', np.NaN],}
    )
    actual = obs_data.clean_access_table(actual)

    expected = pd.DataFrame(
        {'obs_study_id': [91200001, 91200002]}
    )

    assert np.array_equal(actual.values, expected.values)


param_access_exclude = [
    (
        {
            'followup': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'NoUse': [False, False, False, False],
                    'NoContact': [False, False, False, False],
                    'NoAccess': [False, False, False, False],
                    'Fetal Demise/Termination': [False, False, False, False],
                    'Neonatal death': [False, False, False, False],
                    'TwinBDelivery' : [None, None, None, None]
                }
            ),
            'enrolment': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'Previous OBS participant': [False, False, False, False]
                }
            )
        },
        False, #excl_previous_bool
        False, #excl_multiple_bool
        False, #excl_no_use_bool
        False, #excl_no_contact_bool
        False, #excl_no_access_bool
        False, #excl_fetal_demise_bool
        False, #excl_neonatal_death_bool
        []
    ),
    (
        {
            'followup': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'NoUse': [True, False, False, False],
                    'NoContact': [False, False, False, False],
                    'NoAccess': [False, False, False, False],
                    'Fetal Demise/Termination': [False, False, False, False],
                    'Neonatal death': [False, False, False, False],
                    'TwinBDelivery' : [None, None, None, None]
                }
            ),
            'enrolment': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'Previous OBS participant': [False, False, False, False]
                }
            )
        },
        False, #excl_previous_bool
        False, #excl_multiple_bool
        True, #excl_no_use_bool
        False, #excl_no_contact_bool
        False, #excl_no_access_bool
        False, #excl_fetal_demise_bool
        False, #excl_neonatal_death_bool
        [91200001]
    ),
    (
        {
            'followup': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'NoUse': [False, False, False, False],
                    'NoContact': [False, True, False, False],
                    'NoAccess': [False, False, False, False],
                    'Fetal Demise/Termination': [False, False, False, False],
                    'Neonatal death': [False, False, False, False],
                    'TwinBDelivery' : [None, None, None, None]
                }
            ),
            'enrolment': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'Previous OBS participant': [False, False, False, False]
                }
            )
        },
        False, #excl_previous_bool
        False, #excl_multiple_bool
        False, #excl_no_use_bool
        True, #excl_no_contact_bool
        False, #excl_no_access_bool
        False, #excl_fetal_demise_bool
        False, #excl_neonatal_death_bool
        [91200002]
    ),
    (
        {
            'followup': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'NoUse': [False, False, False, False],
                    'NoContact': [False, False, False, False],
                    'NoAccess': [False, False, True, False],
                    'Fetal Demise/Termination': [False, False, False, False],
                    'Neonatal death': [False, False, False, False],
                    'TwinBDelivery' : [None, None, None, None]
                }
            ),
            'enrolment': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'Previous OBS participant': [False, False, False, False]
                }
            )
        },
        False, #excl_previous_bool
        False, #excl_multiple_bool
        False, #excl_no_use_bool
        False, #excl_no_contact_bool
        True, #excl_no_access_bool
        False, #excl_fetal_demise_bool
        False, #excl_neonatal_death_bool
        [91200003]
    ),
    (
        {
            'followup': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'NoUse': [False, False, False, False],
                    'NoContact': [False, False, False, False],
                    'NoAccess': [False, False, False, False],
                    'Fetal Demise/Termination': [False, False, False, True],
                    'Neonatal death': [False, False, False, False],
                    'TwinBDelivery' : [None, None, None, None]
                }
            ),
            'enrolment': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'Previous OBS participant': [False, False, False, False]
                }
            )
        },
        False, #excl_previous_bool
        False, #excl_multiple_bool
        False, #excl_no_use_bool
        False, #excl_no_contact_bool
        False, #excl_no_access_bool
        True, #excl_fetal_demise_bool
        False, #excl_neonatal_death_bool
        [91200004]
    ),
    (
        {
            'followup': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'NoUse': [False, False, False, False],
                    'NoContact': [False, False, False, False],
                    'NoAccess': [False, False, False, False],
                    'Fetal Demise/Termination': [False, False, False, False],
                    'Neonatal death': [True, True, False, False],
                    'TwinBDelivery' : [None, None, None, None]
                }
            ),
            'enrolment': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'Previous OBS participant': [False, False, False, False]
                }
            )
        },
        False, #excl_previous_bool
        False, #excl_multiple_bool
        False, #excl_no_use_bool
        False, #excl_no_contact_bool
        False, #excl_no_access_bool
        False, #excl_fetal_demise_bool
        True, #excl_neonatal_death_bool
        [91200001, 91200002]
    ),
    (
        {
            'followup': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'NoUse': [False, False, False, False],
                    'NoContact': [False, False, False, False],
                    'NoAccess': [False, False, False, False],
                    'Fetal Demise/Termination': [False, False, False, False],
                    'Neonatal death': [False, False, False, False],
                    'TwinBDelivery' : [None, '01/01/1970', '01/01/1970', None]
                }
            ),
            'enrolment': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'Previous OBS participant': [False, False, False, False]
                }
            )
        },
        False, #excl_previous_bool
        True, #excl_multiple_bool
        False, #excl_no_use_bool
        False, #excl_no_contact_bool
        False, #excl_no_access_bool
        False, #excl_fetal_demise_bool
        False, #excl_neonatal_death_bool
        [91200002, 91200003]
    ),
    (
        {
            'followup': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'NoUse': [False, False, False, False],
                    'NoContact': [False, False, False, False],
                    'NoAccess': [False, False, False, False],
                    'Fetal Demise/Termination': [False, False, False, False],
                    'Neonatal death': [False, False, False, False],
                    'TwinBDelivery' : [False, False, False, False]
                }
            ),
            'enrolment': pd.DataFrame(
                {
                    'obs_study_id': [91200001, 91200002, 91200003, 91200004],
                    'Previous OBS participant': [False, False, True, True]
                }
            )
        },
        True, #excl_previous_bool
        False, #excl_multiple_bool
        False, #excl_no_use_bool
        False, #excl_no_contact_bool
        False, #excl_no_access_bool
        False, #excl_fetal_demise_bool
        False, #excl_neonatal_death_bool
        [91200003, 91200004]
    )
]

@pytest.mark.parametrize(
    (
        'access_data_dict, excl_previous_bool, excl_multiple_bool,'
        'excl_no_use_bool, excl_no_contact_bool, excl_no_access_bool,'
        'excl_fetal_demise_bool, excl_neonatal_death_bool,'
        'expected_access_exclude'
    ), param_access_exclude
)

def test_access_exclude(
    access_data_dict, excl_previous_bool, excl_multiple_bool, excl_no_use_bool,
    excl_no_contact_bool, excl_no_access_bool, excl_fetal_demise_bool,
    excl_neonatal_death_bool, expected_access_exclude
    ):
    """Test obs_data.access_exclude"""

    actual = obs_data.access_exclude(
        access_data_dict, excl_previous = excl_previous_bool,
        excl_multiple = excl_multiple_bool, excl_no_use = excl_no_use_bool,
        excl_no_contact = excl_no_contact_bool,
        excl_no_access = excl_no_access_bool,
        excl_fetal_demise = excl_fetal_demise_bool,
        excl_neonatal_death = excl_neonatal_death_bool
    )
    assert(set(actual) == set(expected_access_exclude))
