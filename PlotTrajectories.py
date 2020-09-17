import numpy as np
from matplotlib import pyplot as plt
import re
import json
from ParticleGetter import *
import os

def plotter(ID):
    #first obtain trap coordinates
    fname = '2020-09-16--14-47-43'
    dx, dy, dz = 0.0, 0.0, 0.0 #for uncalibrated traps
    with open(fname + '.json', 'r') as TrapCoord:
        data = TrapCoord.read()
        data = re.sub(r'\s+', '', data)
        data = data[1:-1]
        Xt, Yt, Zt = [], [], []
        counter = 0
        bool = True
        while bool:
            if data != '':
                counter+=1
                #pos = ((data.split('['))[0].split(']')[0]).split(',')
                pos = data.split('[[')[1].split(']]')[0].split(',')
                Xt.append(float(pos[0]) - dx)
                Yt.append(float(pos[1]) - dy)
                Zt.append(float(pos[2]) - dz)
                index = data.find(']]')
                data = data[index+2:]
            else:
                bool = False
        TrapCoord.close()
    print('Trap Coordinates Found')
    #now obtain particle coordinates (if we only have one particle)
    while False:
        with open('your_MLpreds' + '_' + fname + '.json', 'r') as PartCoord:
            PredList = json.load(PartCoord) #pred_list is a list containing dictionaries. Each dict has x_p, y_p, z_p, etc.
        Xp, Yp, Zp = [], [], []
        frame = 0
        for PreDict in PredList: #PreDict...get it?
            Xp.append(PreDict['x_p'])
            Yp.append(PreDict['y_p'])
            Zp.append(PreDict['z_p'])
            frame+=1
            print(frame)
    #If we have multiple particles
    df = find_trajs()
    Xp = [col[1] for row,col in df.iterrows() if col[5] == ID]
    Yp = [col[2] for row,col in df.iterrows() if col[5] == ID]
    Zp = [col[3] for row,col in df.iterrows() if col[5] == ID]
    #plot
    plt.plot(Xt, 'r-')
    plt.plot(Yt, 'b-')
    plt.plot(Zt, 'g-')
    plt.plot(Xp, 'r--')
    plt.plot(Yp, 'b--')
    plt.plot(Zp, 'g--')
    title = 'Trap/Particle Trajectories_' + fname + ' ' + 'Particle ID = ' + str(ID)
    plt.title(title)
    plt.ylabel('Position (pixels)')
    plt.xlabel('Time (frames)')
    plt.legend(('$x_{t}$', '$y_{t}$', '$z_{t}$', '$x_{p}$', '$y_{p}$', '$z_{p}$'))
    folder_path = path + '/trajectories/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    plt.savefig(folder_path + 'trajs_particle_ID#: ' + str(ID) + '.png', dpi = 'figure')

if __name__ == '__main__':
    path = os.getcwd()
    plotter(2) #change the particle ID