#Try to compute the 2D Fourier transform of our function
#same as find_intensity, except this time we are trying to work in physical units

import scipy.special as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines 
from numpy import fft

#work in SI Units
#m = 1
k = 6.905*(10**6) #corresponds to 1064 nm
f = 0.5 
R = 0.09


def find_U0(m, lim):
    #Argument: lim is given in meters (boundaries of our analysis inn x-y plane)
    #Purpose: find fourier transform of the function U_0(x, y, phi,z=0)
    fac = 100; #1/fac is step size in x- and y- directions
    xlist, ylist = [n/fac for n in range(int(-lim*fac),int(lim*fac+1))], [n/fac for n in range(int(-lim*fac),int(lim*fac+1))] #use int() so we can allow for fractional limits
    bessel_array, exp_array = np.zeros((len(xlist), len(ylist)), dtype = "complex"), np.zeros((len(xlist),len(ylist)), dtype = "complex")
    for i in range(len(xlist)):
        for j in range(len(ylist)):
            bessel_array[i,j] = sp.jv(m,k*R/(1*f)*(xlist[i]**2 + ylist[j]**2)**0.5)
            if xlist[i] == 0:
                phi = np.pi/2
            else:
                phi = np.arctan(ylist[j]/xlist[i])
            exp_array[i,j] = np.exp(1j*m*phi)
    holo = bessel_array*exp_array
    U_0 = fft.fft2(bessel_array*exp_array); #FT of holo
    #If we want to plot hologram's intensity:
    #intensity = np.real(holo)**2 + np.imag(holo)**2 
    #plt.imshow(intensity, cmap = 'gray', interpolation = 'nearest', extent=[-lim,lim,-lim,lim])
    #plt.title("FT of Hologram (z=0), m=" + str(m))
    #plt.colorbar()
    #plt.show()
    return U_0 

#2.
def find_Uz(m,z,lim):
    #find the function Uz in real space from U_0 and H
    U_0 = find_U0(m,lim)
    fac = 100
    xlist, ylist = [n/fac for n in range(int(-lim*fac),int(lim*fac+1))], [n/fac for n in range(int(-lim*fac),int(lim*fac+1))]
    H_array = np.zeros((len(xlist),len(ylist)), dtype = "complex")
    for i in range(len(xlist)):
        for j in range(len(ylist)):
            p = xlist[i]*(2*np.pi*fac)
            q = ylist[j]*(2*np.pi*fac)
            s = (p**2+q**2)**0.5
            #print(np.exp(z*1j*(k**2-(2*np.pi*s)**2)**0.5))
            H_array[i,j] = np.exp(z*1j*(k**2-(2*np.pi*s)**2)**0.5) #this expression is FT of h(x,y,z)
    prod = H_array*U_0
    #final step: Find the inverse fourier transform of this guy
    U_z = fft.ifft2(prod)
    Intensity_array = np.real(U_z)**2 + np.imag(U_z)**2
    if False: #Plotting: (change to True if we want to plot)
        plt.figure()
        plt.imshow(((np.imag(U_z)**2))+((np.real(U_z)**2)), cmap = 'gray', interpolation = 'nearest', extent=[-lim,lim,-lim,lim])
        plt.title("Intensity of field at z=" + str(z) + ", " + "m=" + str(m))
        plt.xlabel("x")
        plt.ylabel("y")
        plt.colorbar()
        plt.show(block = False) #so we can display multiple figures to compare
    return Intensity_array

#3
def get_int (coord,m):
    #this function takes in a pair of (x,y) values in meters and outputs an array of intensity values along with corresponding z; m is topological charge
    x,y = coord[0],coord[1]
    z = 0
    zmax = 20*f
    dz = 0.1
    intlist,zlist = list(),list()
    while z < zmax+dz:
        lim = max([x,y])+1 #generate smallest array necessary
        Uz = find_Uz(m,z,lim)
        i = x*2*lim/(np.shape(Uz)[0]-1)
        j = y*2*lim/(np.shape(Uz)[1]-1)
        intensity = np.real(Uz[int(i),int(j)])**2 + np.imag(Uz[int(i),int(j)])**2
        zlist.append(z)
        intlist.append(intensity)
        z+=dz
    fig, ax = plt.subplots(figsize=(8,8))
    ax.scatter(zlist, intlist)
    ax.plot([f,f],[0,max(intlist)],'r--')
    ax.set_title("Intensity of field, " + "m=" + str(m)+ ", for (x,y) = " + str([x,y]))
    ax.set_xlabel("z")
    ax.set_ylabel("Intensity")
    plt.show()
    return intlist
        


#if __name__ == "__main__":
 #   find_Uz(1,0.5,0.5)
        

    
            
    
    
    
            
    
