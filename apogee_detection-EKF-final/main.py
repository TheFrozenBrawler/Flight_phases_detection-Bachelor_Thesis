import numpy as np

import config.config as cfg

from algorithms.KalmanFilter_class import KalmanFilter_class
from algorithms.RealEvents_class import RealEvents_class
from algorithms.FlightStages_class import FlightStages_class
from algorithms.FlightStagesTransitions_class import FlightStagesTransitions_class
from algorithms.noise_adder import precise_noise_adder

from data.plotting import plot_with_matplotlib

noise_presets = {
    "press_normal_sig": cfg.press_normal_sig,
    "press_mach_sig": cfg.press_mach_sig,
    "press_mach_hf_range": cfg.press_mach_hf_range,
    "acc_sig": cfg.acc_sig
}

def main():
    ### INIT
    Tp = cfg.Tp
    RealEvents = RealEvents_class()
    FlightStages = FlightStages_class()
    FSTrans = FlightStagesTransitions_class()

    ### DATA AQCUISITION
    ''' # Time (s); Altitude (m); Vertical velocity (m/s); Vertical acceleration (m/s²); Air pressure (Pa) '''
    t_real, alt_real, vel_real, acc_real, acc_noise, pre_real, pre_noise = precise_noise_adder(cfg.DATA_FILE, noise_presets, Tp, cfg.mach_noise_start, RealEvents, cfg.start_mach_phase)

    # values for pressure preprocessing - CALIBRATION NEEDED
    p0 = pre_noise[0]
    alt0 = alt_real[0]    # in further work it should be somehow calibrated from preesure

    ### MATRIX VALUES
    F = np.array([[ 1, Tp],
                  [ 0, 1]])

    G = np.array([[ Tp ** 2 / 2],
                  [ Tp         ]])

    Q = np.array([[ Tp**4/4, Tp**3/2 ],
                  [ Tp**3/2, Tp**2   ]]) * cfg.acc_var

    P_init = np.array([[ 50, 0 ],
                       [ 0, 50 ]])
    
    P_reset = np.array([[ 100, 0 ],
                       [ 0, 100 ]])

    x_init = np.array([[ 0 ],
                       [ 0 ]])

    ### KALMAN FILTER
    KalmanFilter = KalmanFilter_class(F, G, Q, P_init, x_init, p0, alt0, cfg.T0, cfg.L)

    # data arrays for kalman estimations
    kalman_alt = []
    kalman_vel = []
    P_trace    = []
    R_plot     = []

    # init timestamp
    timestamp = 0

    # first iteration
    KalmanFilter.predict( cfg.acc_init )

    R = cfg.R_nominal
    alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[0], R)

    kalman_alt.append( alt_k )
    kalman_vel.append( vel_k )
    R_plot.append( R )
    P_trace.append( P_t )

    KalmanFilter.predict( acc_noise[0] )

    # iteration loop
    for step in range(1, len(t_real)):
        # manage flight stages for proper Kalman Update

        if FlightStages.flight_stage == FlightStages.STG_THRUSTING:
            R = cfg.R_nominal
            alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[step], R)
            FSTrans.FSTrans_THRUSTING( vel_k, cfg.start_mach_phase, cfg.mach_thres_sampl_nb, timestamp, FlightStages)

        elif FlightStages.flight_stage == FlightStages.STG_E_TRANSONIC_START:
            R = cfg.R_mach
            alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[step], R)
            FSTrans.FSTrans_E_TRANSONIC_START( FlightStages )
        
        elif FlightStages.flight_stage == FlightStages.STG_TRANSONIC:
            R = cfg.R_mach
            alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[step], R)
            FSTrans.FSTrans_TRANSONIC( vel_k, cfg.stop_transonic, cfg.mach_thres_sampl_nb, timestamp, FlightStages)
        
        elif FlightStages.flight_stage == FlightStages.STG_E_TRANSONIC_STOP:
            R = cfg.R_mach
            alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[step], R)
            KalmanFilter.P = P_reset
            FSTrans.FSTrans_E_TRANSONIC_STOP( FlightStages )
        
        elif FlightStages.flight_stage == FlightStages.STG_SMOOTH_P:
            R = cfg.R_mach - (cfg.R_mach - cfg.R_nominal) / (FlightStages.mach_end_time+cfg.mach_smooth_P_time - FlightStages.mach_end_time) * (timestamp - FlightStages.mach_end_time)
            if R < cfg.R_nominal:
                R = cfg.R_nominal
            alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[step], R)
            FSTrans.FSTrans_SMOOTH_P( vel_k, FlightStages.mach_end_time+cfg.mach_smooth_stage_time, cfg.mach_thres_sampl_nb, timestamp, FlightStages)

        elif FlightStages.flight_stage == FlightStages.STG_CRUISING:
            R = cfg.R_nominal
            alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[step], R)
            FSTrans.FSTrans_CRUISING( vel_k, cfg.apogee_thres_sampl_nb, timestamp, FlightStages)
        
        elif FlightStages.flight_stage == FlightStages.STG_E_APOGEE:
            R = cfg.R_nominal
            alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[step], R)
            FSTrans.FSTrans_E_APOGEE( FlightStages )
        
        elif FlightStages.flight_stage == FlightStages.STG_DESCENT:
            R = cfg.R_nominal
            alt_k, vel_k, P_t = KalmanFilter.update( pre_noise[step], R)
            pass

        kalman_alt.append( alt_k )
        kalman_vel.append( vel_k )
        R_plot.append( R )
        P_trace.append( P_t )

        #kalman prediction
        KalmanFilter.predict( acc_noise[step] )

        timestamp += Tp

    ### Quality of estimation
    # RMSE
    alt_rmse = np.sqrt(np.mean((np.array(alt_real) - np.array(kalman_alt))**2))
    print(f"Altitude RMSE: {alt_rmse}")

    ### PLOTTING
    plot_with_matplotlib(t_real, kalman_alt, alt_real, kalman_vel, vel_real, acc_noise, acc_real, P_trace, pre_noise, RealEvents, FlightStages)

if __name__ == "__main__":
    main()
