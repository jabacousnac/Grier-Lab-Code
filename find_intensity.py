#Try to compute the 2D Fourier transform of our function
import scipy.special as sp
import numpy as np
import matplotlib.pyplot as plt
from numpy import fft
from mpl_toolkits.mplot3d import Axes3D

m, k, f, R = 0, 1.0, 1.0, 1.0 #topological charge, wavenumber, focal length, radius of ring

#1.
def find_U0(lim):#lim is the limit on x and on y, i.e x range = [-lim,lim]
    #find fourier transform of the function U_0(x, y, phi,z=0)
    xlist, ylist = list(range(-1*lim,lim+1)), list(range(-1*lim,lim+1))
    bessel_array, exp_array = np.zeros((2*lim+1,2*lim+1), dtype = "complex"), np.zeros((2*lim+1,2*lim+1), dtype = "complex") 
    for i in range(len(xlist)):
        for j in range(len(ylist)):
            bessel_array[i,j] = sp.jv(m,k*R/(1*f)*(xlist[i]**2 + ylist[j]**2)**0.5)
            if xlist[i] == 0:
                phi = np.pi/2
            else:
                phi = np.arctan(ylist[j]/xlist[i])
            exp_array[i,j] = np.exp(1j*m*phi)
    integrand = bessel_array*exp_array
    U_0 = fft.fft2(integrand);
    #debugging stuff:
    #fourier_array = np.real(U_0)**2 + np.imag(U_0)**2 #bessel intensity array (debugging)
    #plt.imshow(fourier_array, cmap = 'gray', interpolation = 'nearest')
    #plt.title("FT of Hologram (z=0), m=" + str(m))
    #plt.show()
    return U_0 #return integrand if we want original function

#2.
def find_Uz(z,lim):
    #find the function Uz in real space from U_0 and H
    U_0 = find_U0(lim);
    H_array = np.zeros((2*lim+1,2*lim+1), dtype = "complex")
    plist, qlist = list(range(-1*lim,lim+1)), list(range(-1*lim,lim+1))
    for i in range(2*lim+1):
        for j in range(2*lim+1):
            s = (plist[i]**2+qlist[j]**2)**0.5    
            H_array[i,j] = np.exp(z*1j*(k**2-(2*np.pi*s)**2)**0.5)
    prod = H_array*U_0
    #final step: Find the inverse fourier transform of this guy
    U_z = fft.ifft2(prod)
    #Plotting:
    #plt.imshow(((np.imag(U_z)**2))+((np.real(U_z)**2)), cmap = 'gray', interpolation = 'nearest')
    #plt.xlabel("x");
    #plt.ylabel("y");
    #plt.colorbar()
    #plt.show()
    return H_array

#3.
#create a heat map which shows intensity along z
def z_int_heatmap(zlim): #zlim is of the form [lowerbound upperbound]
    #call find_Uz to get values for different z's
    lim = 10
    x,y,z,I = [],[],[],[]
    zlist = range(zlim[0],zlim[1])
    xlist,ylist = range(-lim,lim+1), range(-lim,lim+1)
    for q in range(zlim[0],zlim[1]):
        U_z = find_Uz(q,lim) #lim is set to 50 here. Change it if needed
        for i in range(2*lim+1):
            for j in range(2*lim+1):
                x.append(xlist[i])
                y.append(ylist[j])
                z.append(q)
                I.append(np.real(U_z[i][j])**2 + np.imag(U_z[i][j])**2)
    #we've collected the 4D data. Now, plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    print(I)
    img = ax.scatter(x, y, z, c=I, cmap=plt.hot())
    fig.colorbar(img)
    plt.show()
    return
        
        

    
            
    
    
    
            
    
