'''
CONFIG FILE
'''

DATA_FILE_taa = "data/Hexa4+_tp02-alt-acc.csv"
DATA_FILE_tavap = "data/Hexa4+_tp02-alt-vel-acc-pre.csv"
DATA_FILE_w2ms3dg = "Hexa4+_w2ms3dg_tp02-alt-vel-acc-pre.csv"
DATA_FILE_w2ms4dg = "Hexa4+_w2ms4dg_tp02-alt-vel-acc-pre.csv"
DATA_FILE_w5ms4dg = "Hexa4+_w5ms4dg_tp02-alt-vel-acc-pre.csv"
DATA_FILE_w6ms4dg = "Hexa4+_w6ms4dg_tp02-alt-vel-acc-pre.csv"

DATA_FILE = DATA_FILE_tavap

### Noise values
# pressure noise [Pa] - worst case in normal cond. - estimated w/ sensors documentation
press_FFS = 8200
press_FFS_err_p = 0.015
press_normal_sig = press_FFS * press_FFS_err_p / 6  # sigma for Gauss = 20.5 Pa

# Pressure mach noise [Pa] - see OneNote > zaszumienie #
press_mach_sig = 100 * 100    # sigma for Gauss
press_mach_hf_range = 50000  # half-range for uniform distribution

# acceleration noise [m/s²]
acc_sig = 2.5      # sigma for Gauss

# altitude noise [m] - for estimation without preesure sensor
alt_sig = 5        # sigma for Gauss

### ACCELERATION VARIANCES
acc_var = acc_sig**2  # hard case, variance for Kalman

### VELOCITY VALUE TO START MACH NOISE [m/s]
mach_noise_start = 0.7 * 340

### R and R mach adjustment
R_nominal = 100
R_mach     = 10000000
R_adj_vel  = 0.5 * 340

### ACC init
acc_init = 0
