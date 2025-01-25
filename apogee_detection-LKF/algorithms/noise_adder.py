import csv
import random

def mach_noise_adder_gauss(original_data_csv, noise_presets, Tp, mach_noise_start, EventFlags):
    if Tp > 0.02:
        return ValueError("Tp must be less than or equal 0.02")
    timestamp = 0
    t_real    = []
    alt_real  = []
    vel_real  = []
    acc_real  = []
    acc_noise = []
    pre_real  = []
    pre_noise = []

    with open(original_data_csv, "r") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            sim_time = float(row[0])
            alt_r    = float(row[1])
            vel_r    = float(row[2])
            acc_r    = float(row[3])
            pre_r    = float(row[4]) * 100 # mbar to Pa

            while timestamp < sim_time:
                # add noise
                if (vel_r > mach_noise_start):
                    pre_n = random.gauss(pre_r, noise_presets['press_mach_sig'])
                    if not EventFlags.mach_start_flag: # add flag informing about mach start
                        EventFlags.mach_start_flag = True
                        EventFlags.mach_start_time = timestamp
                else:
                    pre_n = random.gauss(pre_r, noise_presets['press_normal_sig'])
                    if EventFlags.mach_start_flag and not EventFlags.mach_end_flag:
                        EventFlags.mach_end_flag = True
                        EventFlags.mach_end_time = timestamp

                acc_n = random.gauss(acc_r, noise_presets['acc_sig'])                
                
                # append data
                t_real.append(timestamp)
                alt_real.append(alt_r)
                vel_real.append(vel_r)
                acc_real.append(acc_r)
                acc_noise.append(acc_n)
                pre_real.append(pre_r)
                pre_noise.append(pre_n)

                timestamp += Tp

    return t_real, alt_real, vel_real, acc_real, acc_noise, pre_real, pre_noise, EventFlags


def mach_noise_adder_uniformdist(original_data_csv, noise_presets, Tp, mach_noise_start, EventFlags):
    if Tp > 0.02:
        return ValueError("Tp must be less than or equal 0.02")
    timestamp = 0
    t_real  = []
    alt_real  = []
    vel_real  = []
    acc_real = []
    acc_noise = []
    pre_real = []
    pre_noise = []

    with open(original_data_csv, "r") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            sim_time = float(row[0])
            alt_r    = float(row[1])
            vel_r    = float(row[2])
            acc_r    = float(row[3])
            pre_r    = float(row[4]) * 100 # mbar to Pa
            
            hf_range_n = noise_presets['press_mach_hf_range']

            while timestamp < sim_time:
                # add noise
                if (vel_r > mach_noise_start):
                    pre_n = random.uniform(pre_r-hf_range_n, pre_r+hf_range_n)
                    if not EventFlags.mach_start_flag: # add flag informing about mach start
                        EventFlags.mach_start_flag = True
                        EventFlags.mach_start_time = timestamp
                else:
                    pre_n = random.gauss(pre_r, noise_presets['press_normal_sig'])
                    if EventFlags.mach_start_flag and not EventFlags.mach_end_flag:
                        EventFlags.mach_end_flag = True
                        EventFlags.mach_end_time = timestamp

                acc_n = random.gauss(acc_r, noise_presets['acc_sig'])                
                
                # append data
                t_real.append(timestamp)
                alt_real.append(alt_r)
                vel_real.append(vel_r)
                acc_real.append(acc_r)
                acc_noise.append(acc_n)
                pre_real.append(pre_r)
                pre_noise.append(pre_n)

                timestamp += Tp

    return t_real, alt_real, vel_real, acc_real, acc_noise, pre_real, pre_noise, EventFlags
