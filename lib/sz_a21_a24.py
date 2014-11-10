import numpy as np

def stull_8_29(dBZ,the_time):
    """
       input:  dBZ : radar feflectivity (dBZ)
               the_time : time in hours
       output: acc_rain: accumulated rain (mm)
              
    """
    a1 = 0.017 #mm/h
    a2 = 0.0714 #/dBZ
    RR = a1*10**(a2*dBZ) 
    acc_rain = RR*the_time
    return acc_rain

letters=['a','b','c','d','e','f'] #assignment letter
dBZ=[15,30,43,50,18,10]
the_time=[0.017,0.25,0.07,0.017,0.42,0.08]

input_vals=zip(dBZ,the_time)

acc_rain=[stull_8_29(x,y) for x,y in input_vals]

output_pairs=zip(letters,acc_rain)

print "\nQuestion A21\n" 
for letter,acc_rain in output_pairs:
    print "%s) %5.3f mm" % (letter,acc_rain)


def stull_8_32(the_wavel,arad_vel):
    """ 
       input:  the_wavel : wavelength (cm)
               arad_vel: average radial velocity (m/s)
       output: dopplershift : (s^-1)
              
    """
    a = 2 #constant (degrees)
    the_wavel = the_wavel/100. #convert cm to m
    dopplershift = a*arad_vel/the_wavel 
    return dopplershift


letters=['a','b','c','d','e','f','g','h'] #assignment letter
arad_vel=[-110,-85,-60,-20,90,65,40,30]
the_wavel=[10,10,10,10,10,10,10,10]

input_vals=zip(the_wavel,arad_vel)

dopplershift=[stull_8_32(wavel,vel) for wavel,vel in input_vals]

output_pairs=zip(letters,dopplershift)

print "\nQuestion A22\n" 
for letter,dopplershift in output_pairs:
    print "%s) %5.0f s^-1" % (letter,dopplershift)
    
def stull_8_36a(Mr,Mr_max):
    
    """
       input
       Mr : radial velocity [m/s]
       Mr_max : maximal radial velocity [m/s]
       output
       Mrf: velocity displayed on the doppler radar
       * negative sign means toward the radar [m/s]
    """
    Mr_false=0    
    
    if (Mr_max < Mr):
        Mr_false = Mr - 2.*Mr_max
    else:
        Mr_false = Mr + 2.*Mr_max     
    return Mr_false
    
question=['a','b','c','d','e','f','g','h','i','j','k','l'] # Question letter
Mr=[26,28,30,35,20,25,55,-26,-28,-30,-35,30]
Mr_max=[25,25,25,25,25,25,25,25,25,25,25,25]
inputs=zip(Mr,Mr_max)
Mrf=[stull_8_36a(x,y) for x,y in inputs]
outputs=zip(question,Mrf)
print "\nQuestion A23\n" 
for question,Mrf in outputs:
    print "%s) %5.0f m/s" % (question,Mrf)
    
    
def R_appear(R_actual,MUR):
    
    """
       input
       R_actual : actual range [m]
       MUR : maximal unambiguous range [m]
       
       
       output
       R_false: false range appearing on the doppler radar [m]
    """
    R_false=R_actual-MUR
        
    return R_false
    
question=['a','b','c','d','e','f','g','h','i','j'] # Question letter
R_actual=[205,210,250,300,350,400,230,240,390,410]
MUR=[200,200,200,200,200,200,200,200,200,200]
inputs=zip(R_actual,MUR)
R_false=[R_appear(x,y) for x,y in inputs]
outputs=zip(question,R_false)
print "\nQuestion A24\n" 
for question,R_false in outputs:
    print "%s) %5.0f m" % (question,R_false)
    
    
    
