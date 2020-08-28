import numpy as np
from matplotlib import pyplot as plt
import re
import json

def plotter():
    #first obtain trap coordinates
    fname = '2020-08-26--14_54_31'
    dx, dy, dz = 0.0, 0.0, 0.0 #for uncalibrated traps
    with open(fname + '.json', 'r') as TrapCoord:
        data = TrapCoord.read()
        data = re.sub(r'\s+', '', data)
        Xt, Yt, Zt = [], [], []
        bool = True
        while bool:
            if data != '':
                pos = ((data.split('['))[1].split(']')[0]).split(',')
                Xt.append(float(pos[0]) - dx)
                Yt.append(float(pos[1]) - dy)
                Zt.append(float(pos[2]) - dz)
                index = data.find(']')
                data = data[index + 1:]
            else:
                bool = False
        TrapCoord.close()
    #now obtain particle coordinates
    with open('your_MLpreds.json', 'r') as PartCoord:
        PredList = json.load(PartCoord) #pred_list is a list containing dictionaries. Each dict has x_p, y_p, z_p, etc.
    Xp, Yp, Zp = [], [], []
    for PreDict in PredList: #PreDict...get it?
        Xp.append(PreDict['x_p'])
        Yp.append(PreDict['y_p'])
    #plot
    plt.figure(0)
    plt.plot(Xt, 'r-')
    plt.plot(Yt, 'b-')
    plt.plot(Zt, 'g-')
    plt.plot(Xp, 'r--')
    plt.plot(Yp, 'b--')
    plt.plot(Zp, 'g--')
    plt.title('Trap/Particle Trajectories')
    plt.ylabel('Position (pixels)')
    plt.xlabel('Time (frames)')
    plt.legend(('$x_{t}$', '$y_{t}$', '$z_{t}$', '$x_{p}$', '$y_{p}$', '$z_{p}$'))
    plt.show()

if __name__ == '__main__':
    plotter()