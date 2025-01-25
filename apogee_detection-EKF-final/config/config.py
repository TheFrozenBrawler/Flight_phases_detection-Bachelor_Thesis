'''
CONFIG FILE
'''

DATA_FILE_taa = "data/Hexa4+_tp02-alt-acc.csv"
DATA_FILE_tavap = "data/Hexa4+_tp02-alt-vel-acc-pre.csv"
DATA_FILE_tavap_cut = "data/Hexa4+_tp02-alt-vel-acc-pre-CUT.csv"
DATA_FILE_w2ms3dg = "data/Hexa4+_w2ms3dg_tp02-alt-vel-acc-pre.csv"
DATA_FILE_w2ms4dg = "data/Hexa4+_w2ms4dg_tp02-alt-vel-acc-pre.csv"
DATA_FILE_w5ms4dg = "data/Hexa4+_w5ms4dg_tp02-alt-vel-acc-pre.csv"
DATA_FILE_w6ms4dg = "data/Hexa4+_w6ms4dg_tp02-alt-vel-acc-pre.csv"

DATA_FILE = DATA_FILE_tavap

# TIME SAMPLING [s]
Tp = 0.02

# NOISE VALUES
## pressure noise [Pa] - worst case in normal cond. - estimated w/ sensors documentation
press_FFS = 8200
press_FFS_err_p = 0.015
press_normal_sig = press_FFS * press_FFS_err_p / 6  # sigma for Gauss = 20.5 Pa

## Pressure mach noise [Pa] - see OneNote > zaszumienie #
press_mach_sig = 100 * 100    # sigma for Gauss
press_mach_hf_range = 50000  # half-range for uniform distribution

## acceleration noise [m/s²]
acc_sig = 2.5

# ACCELERATION VARIANCES
acc_var = acc_sig**2

# VELOCITY VALUE TO START MACH NOISE [m/s]
mach_noise_start = 0.8 * 340

# R and R mach adjustment
R_nominal = 100
R_mach     = 10000000
start_mach_phase  = 0.65 * 340  # if the estimated velocity is above this value, the mach phase starts
stop_transonic  = 0.7 * 340 
mach_thres_sampl_nb = 10
mach_smooth_P_time = 4  #[s]
mach_smooth_stage_time = 9  #[s]

# Apogee detection
apogee_thres_sampl_nb = 30

# ACC init
acc_init = 0

# PRESSURE CALCULATION
L = -0.0065
T0 = 15
