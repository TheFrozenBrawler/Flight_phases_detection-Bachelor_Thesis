'''
This file aims for computing only the model values of 
Kalman filter. It is used to compare the model values and
to study different types of models and their characteristics.
'''

import numpy as np
from noise_adder import gauss_mach_zoh_noise_adder
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))

import config as cfg


DATA_FILE = "data/Hexa4+_tp02-alt-vel-acc-pre.csv"
Tp = 0.02
noise_presets = {
    "press_normal_sig": cfg.alt_sig,
    "press_mach_sig": cfg.press_mach_sig,
    "acc_sig": cfg.acc_sig_easy
}

F = np.array([[ 1, Tp],
              [ 0, 1]])

G = np.array([[ Tp ** 2 / 2],
              [ Tp         ]])

x = np.array([[ 0 ],
              [ 0 ]])

t_real, alt_real, vel_real, acc_real, acc_noise, pre_real, pre_noise = gauss_mach_zoh_noise_adder(DATA_FILE, noise_presets, Tp, cfg.mach_noise_start)

alt_model= []

''' with ZOH implemented in noise_adder.py'''
for step in range(0, len(alt_real)):

    #model calculations
    x = F @ x + G * (acc_real[step])
    alt_model.append(x[0][0])
  
plt.plot(alt_model, 'b', label='Model')
plt.plot(alt_real, 'r', label='Real')
plt.legend()
plt.grid()
plt.show()
