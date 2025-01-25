import matplotlib.pyplot as plt

### PLOTTING
def plot_with_matplotlib(t_real, alt_meas, kalman_alt, alt_real, kalman_vel, vel_real, acc_noise, acc_real, P_trace, pre_noise, EventFlags):
    # altitude
    plt.subplot(4, 1, 1)
    plt.plot(t_real, alt_meas, '.g', label="altitude measurements")     #noised altitiude
    plt.plot(t_real, kalman_alt, 'b', label="estimated altitude")  #kalman altitiude
    plt.plot(t_real, alt_real, '--r', label="real height (ZOH)")      #measured altitiude
    plt.axvline(x=EventFlags.mach_start_time, color='purple', linestyle='--', label="mach start")
    plt.axvline(x=EventFlags.mach_end_time, color='pink', linestyle='--', label="mach start")
    plt.xlabel("Time [s]")
    plt.ylabel("Altitude [m]")
    plt.legend(loc='upper right')
    plt.grid()

    # velocity
    plt.subplot(4, 1, 2)
    plt.plot(t_real, kalman_vel, 'b', label="estimated velocity")
    plt.plot(t_real, vel_real, '--r', label="real velocity")
    plt.axvline(x=EventFlags.mach_start_time, color='purple', linestyle='--', label="mach start")
    plt.axvline(x=EventFlags.mach_end_time, color='pink', linestyle='--', label="mach start")
    plt.xlabel("Time [s]")
    plt.ylabel("velocity [m/s]")
    plt.legend(loc='upper right')
    plt.grid()

    # acceleration
    plt.subplot(4, 1, 3)
    plt.plot(t_real, acc_noise, '.m', label="acceleration with noise")
    plt.plot(t_real, acc_real, 'g', label="real acceleration")
    plt.axvline(x=EventFlags.mach_start_time, color='purple', linestyle='--', label="mach start")
    plt.axvline(x=EventFlags.mach_end_time, color='pink', linestyle='--', label="mach start")
    plt.xlabel("Time [s]")
    plt.ylabel("Acceleration [m/s^2]")
    plt.legend(loc='upper right')
    plt.grid()

    # p trace
    plt.subplot(4, 1, 4)
    ax1 = plt.gca()
    ax2 = ax1.twinx()

    ax2.plot(t_real, pre_noise, '.r', label="pressure noise")
    ax1.plot(t_real, P_trace, 'b', label="P matrix trace")
    plt.axvline(x=EventFlags.mach_start_time, color='purple', linestyle='--', label="mach start")
    plt.axvline(x=EventFlags.mach_end_time, color='pink', linestyle='--', label="mach start")
    ax1.set_xlabel("Time [s]")
    ax2.set_ylabel("Pressure noise", color='r')
    ax1.set_ylabel("P matrix trace", color='b')

    ax2.legend(loc='upper right')
    ax1.legend(loc='upper left')
    ax1.grid()

    plt.show()
