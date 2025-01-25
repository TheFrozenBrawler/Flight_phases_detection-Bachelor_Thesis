from enum import Enum

# STG - stage of flight
# STG_E - event in flight
class FlightStages_class():
    def __init__(self):
        self.flight_stage = self.STG_THRUSTING

        self.mach_start_time = None
        self.mach_end_time = None
        self.apogee_time = None

    STG_THRUSTING           = 0
    STG_E_TRANSONIC_START   = 1
    STG_TRANSONIC           = 2
    STG_E_TRANSONIC_STOP    = 3
    STG_SMOOTH_P            = 4
    STG_CRUISING            = 5
    STG_E_APOGEE            = 6
    STG_DESCENT             = 7
