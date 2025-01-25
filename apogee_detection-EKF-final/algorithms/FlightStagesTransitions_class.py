class FlightStagesTransitions_class:
    def __init__(self):
        self.estim_mach_start_counter = 0        
        self.estim_mach_end_counter = 0
        self.estim_apogee_counter = 0
        self.estim_trans_end_counter = 0

    ''' Functions below contains conditions for transitions between flight stages 
        E - event in flight that automatically triggers the next stage'''
    def FSTrans_THRUSTING(self, est_vel, start_mach_phase, mach_thres_sampl_nb, timestamp, FlightStages): 
        # conditions of phase end:
        if est_vel > start_mach_phase:
            self.estim_mach_start_counter += 1
            if self.estim_mach_start_counter == mach_thres_sampl_nb:
                FlightStages.mach_start_time = timestamp
                FlightStages.flight_stage = FlightStages.STG_E_TRANSONIC_START

    def FSTrans_E_TRANSONIC_START(self, FlightStages):
        FlightStages.flight_stage = FlightStages.STG_TRANSONIC

    def FSTrans_TRANSONIC(self, est_vel, v_stop_transonic, mach_thres_sampl_nb, timestamp, FlightStages):
        # conditions of phase end:
        if est_vel < v_stop_transonic:
            self.estim_mach_end_counter += 1
            if self.estim_mach_end_counter == mach_thres_sampl_nb:
                FlightStages.mach_end_time = timestamp
                FlightStages.flight_stage = FlightStages.STG_E_TRANSONIC_STOP

    def FSTrans_E_TRANSONIC_STOP(self, FlightStages):
        FlightStages.flight_stage = FlightStages.STG_SMOOTH_P

    def FSTrans_SMOOTH_P(self, est_vel, smooth_stage_stop_time, mach_thres_sampl_nb, timestamp, FlightStages):
        # conditions of phase end:
        if timestamp > smooth_stage_stop_time:
            self.estim_trans_end_counter += 1
            if self.estim_trans_end_counter == mach_thres_sampl_nb:
                FlightStages.flight_stage = FlightStages.STG_CRUISING

    def FSTrans_CRUISING(self, est_vel, apogee_thres_sampl_nb, timestamp, FlightStages):
        # conditions of phase end:
        if est_vel <= 0:
            self.estim_apogee_counter += 1
            if self.estim_apogee_counter == apogee_thres_sampl_nb:
                FlightStages.apogee_time = timestamp
                FlightStages.flight_stage = FlightStages.STG_E_APOGEE
    
    def FSTrans_E_APOGEE(self, FlightStages):
        FlightStages.flight_stage = FlightStages.STG_DESCENT
