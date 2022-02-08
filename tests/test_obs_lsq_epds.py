"""Tests for obs_lsq_epds module"""

import pandas as pd
import obs_lsq_epds
import obs_data

def test_Lsq2Epds_init(monkeypatch):
    """Test obs_lsq_epds.Lsq2Epds.__init__"""

    def mock_df(*args, **kwargs):
        """Create mock dataframe for monkeypatch"""
        mock_df = pd.DataFrame(
            {
                'obs_study_id': ['10100001', '10100003'],
                'lwk_funny': ['4', '1'],
                'lwk_lookfo': ['4', '1'],
                'lwk_blame': ['2', '1'],
                'lwk_anxio': ['4', '1'],
                'lwk_scare': ['1', '1'],
                'lwk_top': ['1', '1'],
                'lwk_sleep': ['1', '1'],
                'lwk_miser': ['2', '1'],
                'lwk_cryin': ['1', '1'],
                'lwk_harm': ['1', '1']
            }
        )

        return mock_df
    monkeypatch.setattr(obs_data, 'redcap_data', mock_df)

    actual = obs_lsq_epds.Lsq2Epds(
        obs_ids = ['10100001'],
        api_param = None,
        cut_off = 10
    )

    assert all(actual.redcap_lsq2['obs_study_id'] == ['10100001', '10100003'])
    assert actual.fu_ids == [['10100001', 30, 'Yes, quite often']]


def test_Lsq3Epds_init(monkeypatch):
    """Test obs_lsq_epds.Lsq3Epds.__init__"""

    def mock_df(*args, **kwargs):
        """Create mock dataframe for monkeypatch"""
        mock_df = pd.DataFrame(
            {
                'obs_study_id': ['10100001', '10100003'],
                'lweek_laugh': ['4', '1'],
                'lweek_enjoy': ['4', '1'],
                'lweek_blame': ['2', '1'],
                'lweek_anxious': ['4', '2'],
                'lweek_panic': ['1', '1'],
                'lweek_top': ['1', '1'],
                'lweek_unhappy': ['1', '1'],
                'lweek_miserable': ['1', '3'],
                'lweek_crying': ['1', '1'],
                'lweek_harming': ['4', '4']
            }
        )

        return mock_df
    monkeypatch.setattr(obs_data, 'redcap_data', mock_df)

    actual = obs_lsq_epds.Lsq3Epds(
        obs_ids = ['10100001'],
        api_param = None,
        cut_off = 10
    )

    assert all(actual.redcap_lsq3['obs_study_id'] == ['10100001', '10100003'])
    assert actual.fu_ids == [['10100001', 30, 'Yes, quite often']]
