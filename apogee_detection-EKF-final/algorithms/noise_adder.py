import csv
import random

def precise_noise_adder(original_data_csv, noise_presets, Tp, mach_noise_start, RealEvents, start_mach_phase):
    if Tp > 0.02:
        return ValueError("Tp must be less than or equal 0.02")
    timestamp   = 0
    t_real      = []
    alt_real    = []
    vel_real    = []
    acc_real    = []
    acc_noise   = []
    pre_real    = []
    pre_noise   = []

    with open(original_data_csv, "r") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            sim_time = float(row[0])
            alt_r    = float(row[1])
            vel_r    = float(row[2])
            acc_r    = float(row[3])
            pre_r    = float(row[4]) * 100 # convert mbar to Pa
            
            hf_range_n = noise_presets['press_mach_hf_range']
            normal_sig = noise_presets['press_normal_sig']

            while timestamp < sim_time:
                # add noise
                if (vel_r > 0.9*340):
                    pre_n = random.uniform(pre_r-hf_range_n, pre_r+hf_range_n)
                elif (vel_r > mach_noise_start):
                    noise_range = normal_sig + (hf_range_n - normal_sig) * ((vel_r - mach_noise_start) / (0.9 * 340 - mach_noise_start))
                    pre_n = random.uniform(pre_r-noise_range, pre_r+noise_range)
                    if not RealEvents.real_mach_n_start_flag:
                        RealEvents.real_mach_n_start_flag = True
                        RealEvents.real_mach_n_start_time = timestamp
                else:
                    pre_n = random.gauss(pre_r, normal_sig)
                    if RealEvents.real_mach_n_start_flag and not RealEvents.real_mach_n_end_flag:
                        RealEvents.real_mach_n_end_flag = True
                        RealEvents.real_mach_n_end_time = timestamp

                acc_n = random.gauss(acc_r, noise_presets['acc_sig'])                


                if vel_r > start_mach_phase and not RealEvents.real_mach_phase_start_flag:
                    RealEvents.real_mach_phase_start_flag = True
                    RealEvents.real_mach_phase_start_time = timestamp
                elif vel_r < start_mach_phase and not RealEvents.real_mach_phase_end_flag and RealEvents.real_mach_phase_start_flag:
                    RealEvents.real_mach_phase_end_flag = True
                    RealEvents.real_mach_phase_end_time = timestamp

                elif vel_r <= 0 and not RealEvents.real_apogee_flag and RealEvents.real_mach_phase_end_flag:
                    RealEvents.real_apogee_flag = True
                    RealEvents.real_apogee_time = timestamp
                
                # append data
                t_real.append(timestamp)
                alt_real.append(alt_r)
                vel_real.append(vel_r)
                acc_real.append(acc_r)
                acc_noise.append(acc_n)
                pre_real.append(pre_r)
                pre_noise.append(pre_n)

                timestamp += Tp

    return t_real, alt_real, vel_real, acc_real, acc_noise, pre_real, pre_noise
