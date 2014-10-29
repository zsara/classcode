from __future__ import division
import numpy as np

def beamwidth(wavelength,dish_diam):
    """
    Chapter 8 problem A10
    Find the beamwidth angle (delta beta)for a radar pulse
    for the following sets of [wavelength (cm) , antenna
    dish diameter (m)]
    input: wavelength -- wavelength in cm
    dish_diam -- atenna dish diameter in m
    output: beamwitdth -- beamwitdth in degrees
    """
    wavelength=np.array[20,20,10,10,10,5,5,5,5,3]
    wavelength=wavelength*1.e-2 #convert to meters
    dish_diam=np.array[8,10,10,5,3,7,5,2,3,1]
    """
    use equation 8.13 from Stull to calculate the beamwidth, delta beta.
		
    delta_beta=a*lambda/(diameter of dish)
    a=71.6 degrees
    beamwidth=a*wavelength/dish_diam
    """
    a=71.6	#degrees
    beamwidth=a*(wavelength/dish_diam)
    return beamwidth
	
    """
	Chapter 8 problem A11
	What is the name of the radar band associated
	with the wavelengths of the previous exercise?

	Answer:
	wavelengths 2.5-3.75cm = X band
	wavelengths 3.75-7.5cm = C band
	wavelengths 7.5-15cm   = S band
    """
def range(travel_time):
    """
    Chapter 8 problem A12
    Find the range to a radar target, given the
    round-trip (return) travel times (µs) of:
    input: travel_time -- travel time in µs
    output:  range -- range in m
    use equation 8.16 from Stull to calculate the range 
    R=c*t/2
    """
    c=3*10**8	#m/s
    travel_time=np.array[2,5,10,25,50,75,100,150,200,300]
    travel_time=travel_time*1.e-6 #covert to seconds
    range=c*travel_time/2
    return range
	
def MUR(PRF):
    """
    Chapter 8 problem A13
    Find the radar max unambiguous range for
    pulse repetition frequencies (s^1) of:
    input: PRF -- pulse repetition frequency s^-1
    output: MUR -- max unambiguous range m
    use equation 8.17 from Stull to calculate the MUR
    MUR=c/(2*PRF)
	"""
    c=3*10**8	#m/s
    PRF=np.array[50,100,200,400,600,800,1000,1200,1400,1600]
    PRF=PRF*1000 #covert to meters
    MUR=c/(2*PRF)
    return MUR

def Mrmax(wavelength,PRF):
    """
	Chapter 8 problem A14
	Find the Doppler max unambiguous velocity
	for a radar with pulse repetition frequency (s^1) as
	given in the previous exercise, for radar with wavelength
	of:
       input: PRF--freq-- pulse repetition frequency s^-1
			  wavelength -- wavelength in m
       output: mrmax -- Maximum Unambiguous Velocity m/s
	use equation 8.35 from Stull to calculate the Mrmax
	Mrmax=wavelenght*PRF/4
	"""
    PRF=np.array[50,100,200,400,600,800,1000,1200,1400,1600]
    wavelength=[10,5]  #??
    Mrmax=wavelength*PRF/4
    return Mrmax
	
	
def MUV_max(wavelength,PRF):
    """
	Chapter 8 problem A14
	Find the Doppler max unambiguous velocity
	for a radar with pulse repetition frequency (s^–1) as
	given in the previous exercise, for radar with wavelength
	of:
       input: PRF -- pulse repetition frequency s^-1
			  wavelength -- wavelength in cm
       output: mrmax -- Maximum Unambiguous Velocity m/s
	use equation 8.35 from Stull to calculate the Mrmax
	Mrmax=wavelenght*PRF/4
    """
    MUV_max=np.zeros((len(PRF),len(wavelength)))
    wavelength=wavelength*1.e-2 #convert to meters
    
    wavelength_A14=np.array([10,5])
    PRF=np.array([50,100,200,400,600,800,1000,1200,1400,1600])

    MUV_max=MUV_max(wavelength_A14,PRF)
    
    for i in range(0,len(wavelength)):
        MUV_max[:,i]=wavelength[i]*PRF/4
        
    return MUV_max