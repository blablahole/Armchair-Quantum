from __future__ import division
import math
 # Python Code Ex15.4 Photoelectric effect in a photocell: Page-487 (2010)
  
#Variable declaration


e = 1.602e-019; # Charge on an electron, C
h = 6.626e-034; # Planck's constant, Js
c = 3.0e+08; # Speed of light in vacuum, m/s
lamb = 1849e-010; # Wavelength of incident light, m
V_0 = 2.72; # Stopping potential for emitted electrons, V


#Calculation

f = c/lamb; # Frequency of incident radiation , Hz
E = h*f; # Energy carried by one photon from Planck's law, J
T_max = e*V_0; # Maximum kinetic energy of electrons, J
 # We have, T_max = E - h*f_0 = h*f - W
f_0 = (-T_max + E )/h # Threshold frequency for Cu metal, Hz
W = h*f_0/e; # Work function of Cu metal, eV



#Result

print ("\nThrehold frequency for Cu metal =",round((f_0*10**-14),2)*10**14," Hz")
print ("\nThe work function of Cu metal = ",round(W)," eV")
print ("\nThe maximum kinetic energy of photoelectrons =",round(T_max/e,2)," eV")