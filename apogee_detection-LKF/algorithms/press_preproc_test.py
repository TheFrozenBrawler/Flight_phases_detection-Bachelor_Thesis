'''
This file tests the altitude estimation from
pressure measurements. It uses the pressure_preprocessing
function. It was used to write the function and to test it.
'''

import csv
from pressure_preprocessing import pressure_preprocessing
from matplotlib import pyplot as plt

alt_real = []
press = []
t = []


# with open("data/Hexa4+_tp02-alt-vel-acc-pre.csv", "r") as file:
with open("data/Hexa4+_tp02-alt-vel-acc-pre.csv", "r") as file:
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        t.append( float(row[0]) )
        alt_real.append( float(row[1]) )
        
        p_mbar = float(row[4])
        p_pa = p_mbar*100 # mbar to Pa
        press.append( p_pa )

p0 = press[0]
h0 = alt_real[0]
pressRMS = 0 # altitude estimation quality

alt_preproc = []
for n in range(len(press)):
    alt_preproc.append( pressure_preprocessing(press[n], p0, h0) )
    pressRMS += (alt_preproc[n] - alt_real[n])**2
pressRMS = (pressRMS / len(press))**(1/2)
print(pressRMS)

plt.plot(t, alt_real, 'r', label="real altitude")
plt.plot(t, alt_preproc, 'b', label="counted altitude")

plt.xlabel("Time [s]")
plt.ylabel("Altitude [m]")
plt.legend()
plt.grid()
plt.show()
