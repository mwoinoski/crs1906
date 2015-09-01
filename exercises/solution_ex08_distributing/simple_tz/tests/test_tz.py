"""
test_tz.py - Unit tests for simple_tz.tz
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from simple_tz import tz


def test_simple_tz_na_timezones():
    """Convert EST to/from PST"""
    ny_time = '2016-01-01 18:00:00'
    bc_time = '2016-01-01 15:00:00'

    ny_to_bc = tz.convert(ny_time, from_tz='EST', to_tz='PST')
    bc_to_ny = tz.convert(bc_time, from_tz='PST', to_tz='EST')

    assert ny_to_bc == bc_time
    assert bc_to_ny == ny_time


def test_simple_tz_na_daylist_saving_timezones():
    """Convert EDT to/from PDT"""
    ny_time = '2016-01-01 18:00:00'
    bc_time = '2016-01-01 15:00:00'

    ny_to_bc = tz.convert(ny_time, from_tz='EDT', to_tz='PDT')
    bc_to_ny = tz.convert(bc_time, from_tz='PDT', to_tz='EDT')

    assert ny_to_bc == bc_time
    assert bc_to_ny == ny_time


def test_simple_tz_eur_timezones():
    """Convert EST to/from PST"""
    gmt_time = '2016-01-01 18:00:00'
    cet_time = '2016-01-01 19:00:00'

    gmt_to_cet = tz.convert(gmt_time, from_tz='GMT', to_tz='CET')
    cet_to_utc = tz.convert(cet_time, from_tz='CET', to_tz='GMT')

    assert gmt_to_cet == cet_time
    assert cet_to_utc == gmt_time
