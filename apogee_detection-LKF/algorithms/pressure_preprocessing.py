'''
This formula and it's values were
taken from CATS manual.
'''
L = -0.0065
T0 = 15

def pressure_preprocessing(p_pa, p0_pa, alt0_m):
    alt = ( (p_pa/p0_pa)**(1/5.257) - 1 ) * (T0+273.15)/L - alt0_m

    return alt
