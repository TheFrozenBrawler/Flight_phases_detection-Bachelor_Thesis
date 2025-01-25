// config.h
#ifndef CONFIG_H
#define CONFIG_H

// Data file paths
#define DATA_FILE "data/Hexa4+_tp02-alt-vel-acc-pre.csv"

// Time sampling [s]
#define TP 0.02f

// Noise values
#define PRESS_FFS 8200
#define PRESS_FFS_ERR_P 0.015f
#define PRESS_NORMAL_SIG (PRESS_FFS * PRESS_FFS_ERR_P / 6.0f) // Sigma for Gauss
#define PRESS_MACH_SIG (100 * 100)  // Sigma for Gauss
#define PRESS_MACH_HF_RANGE 50000  // Half-range for uniform distribution

// Acceleration noise [m/s²]
#define ACC_SIG 1.6f  // sigma for Gauss

// Acceleration variances
#define ACC_VAR (ACC_SIG * ACC_SIG)  // Easy case, variance for Kalman

// Velocity value to start Mach noise [m/s]
#define MACH_NOISE_START (0.8f * 340.0f)

// R and R Mach adjustment
#define R_NOMINAL 100.0f
#define R_MACH 10000000.0f
#define START_MACH_PHASE (0.65f * 340.0f)
#define STOP_TRANSONIC (0.7f * 340.0f)
#define MACH_THRES_SAMPL_NB 10
#define MACH_SMOOTH_P_TIME 4.0f  // [s]
#define MACH_SMOOTH_STAGE_TIME 9.0f  // [s]

// Apogee detection
#define APOGEE_THRES_SAMPL_NB 30

// Initial acceleration
#define ACC_INIT 0.0f

// Pressure calculation
#define L -0.0065f
#define T0 15.0f
#define PRESSURE_START 101325.0f
#define ALTITUDE_START 0.0f
#define VELOCITY_START 0.0f

#endif // CONFIG_H
