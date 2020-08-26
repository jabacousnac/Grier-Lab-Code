import numpy as np
from matplotlib import pyplot as plt
import re

def plotter():
    fname = '2020-08-21--20_25_04'
    dx, dy, dz = 0.0, 0.0, 0.0 #for uncalibrated traps
    with open(fname + '.json', 'r') as myFile:
        data = myFile.read()
        data = re.sub(r'\s+', '', data)
        X, Y, Z = [], [], []
        bool = True
        while bool:
            if data != '':
                pos = ((data.split('['))[1].split(']')[0]).split(',')
                X.append(float(pos[0]) - dx)
                Y.append(float(pos[1]) - dy)
                Z.append(float(pos[2]) - dz)
                index = data.find(']')
                data = data[index + 1:]
            else:
                bool = False
    plt.figure(0)
    plt.plot(X, 'r-')
    plt.plot(Y, 'b-')
    plt.plot(Z, 'g-')
    plt.title('Trap Trajectory')
    plt.ylabel('Position (pixels)')
    plt.xlabel('Time (frames)')
    plt.legend(('x', 'y', 'z'))
    plt.show()
    return

if __name__ == '__main__':
    plotter()