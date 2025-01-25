import numpy as np

import config.config as cfg

from algorithms.KalmanFilter_class import KalmanFilter
from algorithms.EventFlags_class import EventFlags_class

from algorithms.noise_adder import mach_noise_adder_gauss, mach_noise_adder_uniformdist
from algorithms.pressure_preprocessing import pressure_preprocessing

from data.plotting import plot_with_matplotlib

'''
The Kalman Filter won't work with gaussian_noise_adder
due to the sampling time of simulated data, which is not constant.

In gauss_nos_zoh_adder, the data is interpolated to have a constant sampling time.
'''

### CONFIG
Tp = 0.02

noise_presets = {
    "press_normal_sig": cfg.press_normal_sig,
    "press_mach_sig": cfg.press_mach_sig,
    "press_mach_hf_range": cfg.press_mach_hf_range,
    "acc_sig": cfg.acc_sig
}

def main():
    EventFlags = EventFlags_class()

    ### DATA AQCUISITION
    ''' # Time (s); Altitude (m); Vertical velocity (m/s); Vertical acceleration (m/s²); Air pressure (Pa) '''
    # t_real, alt_rel, alt_nos, acc_rel, acc_nos = gauss_nos_zoh_adder(cfg.DATA_FILE_taa, noise_presets, Tp) # gaussian_noise_adder(cfg.DATA_FILE, noise_presets)
    t_real, alt_real, vel_real, acc_real, acc_noise, pre_real, pre_noise, EventFlags = mach_noise_adder_uniformdist(cfg.DATA_FILE, noise_presets, Tp, cfg.mach_noise_start, EventFlags)

    # values for pressure preprocessing
    p0 = pre_noise[0]
    h0 = alt_real[0]

    ### MATRIX VALUES
    F = np.array([[ 1, Tp],
                  [ 0, 1]])

    G = np.array([[ Tp ** 2 / 2],
                  [ Tp         ]])

    H = np.array([ 1, 0])

    Q = np.array([[ Tp**4/4, Tp**3/2 ],
                  [ Tp**3/2, Tp**2   ]]) * cfg.acc_var

    P_init = np.array([[ 50, 0 ],
                       [ 0, 50 ]])

    x_init = np.array([[ 0 ],
                       [ 0 ]])

    ### KALMAN FILTER
    kalman = KalmanFilter(F, G, H, Q, P_init, x_init)

    # data arrays for kalman estimations
    kalman_alt = []
    kalman_vel = []
    alt_meas   = []
    P_trace    = []

    # first iteration
    kalman.predict( cfg.acc_init )
    alt_p = pressure_preprocessing(pre_noise[0], p0, h0)
    alt_meas.append(alt_p)

    alt_k, vel_k, P_t = kalman.update( alt_meas[0], cfg.R_nominal )

    kalman_alt.append( alt_k )
    kalman_vel.append( vel_k )
    P_trace.append( P_t )

    kalman.predict( acc_noise[0] )

    # iteration loop
    for step in range(1, len(t_real)):
        # preprocess
        alt_p = pressure_preprocessing(pre_noise[step], p0, h0)
        alt_meas.append(alt_p)

        # adjust R for mach noise
        # kalman update and data estimation
        if kalman_vel[step-1] > cfg.R_adj_vel:
            alt_k, vel_k, P_t = kalman.update( alt_meas[step], cfg.R_mach )
        else:
            alt_k, vel_k, P_t = kalman.update( alt_meas[step], cfg.R_nominal )

        kalman_alt.append( alt_k )
        kalman_vel.append( vel_k )
        P_trace.append( P_t )

        #kalman prediction
        kalman.predict( acc_noise[step] )

    ### Quality of estimation
    # RMSE
    alt_rmse = np.sqrt(np.mean((np.array(alt_real) - np.array(kalman_alt))**2))
    print(f"Altitude RMSE: {alt_rmse}")

    ### PLOTTING
    plot_with_matplotlib(t_real, alt_meas, kalman_alt, alt_real, kalman_vel, vel_real, acc_noise, acc_real, P_trace, pre_noise, EventFlags)

if __name__ == "__main__":
    main()
