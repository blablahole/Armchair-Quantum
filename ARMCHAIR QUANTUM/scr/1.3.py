import scipy.constants as constant
print (constant.h)
print (constant.c)

#Variables and constants 
e = 1.602e-019; # Charge on an electron, C
lamb = 1849e-010; # Wavelength of incident light, m
V_0 = 2.72; # Stopping potential for emitted electrons, V

import scipy.constants as constant
from __future__ import division
import math 


#Calculation
f = constant.c/lamb; # Frequency of incident radiation , Hz
E = constant.h*f; # Energy carried by one photon from Planck's law, J
T_max = e*V_0; # Maximum kinetic energy of electrons, J
 # We have, T_max = E - h*f_0 = h*f - W
f_0 = (-T_max + E )/h # Threshold frequency for Cu metal, Hz
W = h*f_0/e; # Work function of Cu metal, eV

#Result
print("\nThrehold frequency for Cu metal =",round((f_0*10**-14),10)*10**14,"Hz")
print("\nThe work function of Cu metal = ",round(W),"eV")
print("\nThe maximum kinetic energy of photoelectrons =",round(T_max/e,2),"eV")