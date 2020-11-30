from matplotlib import pyplot as plt
import re
import json
from ParticleGetter import *
import os
import numpy as np

def plotter(ID):
    #first obtain trap coordinates
    fname = '2020-11-13--17-08-57'
    trap_ID = 1 #there are n traps and we can choose one of these traps
    dx, dy, dz = 0.0, 0.0, 0.0 #for uncalibrated traps
    with open(fname + '.json', 'r') as TrapCoord:
        data = TrapCoord.read()
        data = re.sub(r'\s+ ', '', data)
        data = data[1:-1]
        Xt, Yt, Zt = [], [], []
        counter = 0
        bool = True
        while bool:
            if data != '':
                counter+=1
                my_index = data.find(']]')
                frame = data[1:my_index+1] #this is trap coordinates [x1,y1,z1], [x2,y2,z2] for frame
                #now, we have to splice frame to get trap coordinates of interest
                #we get a new data:
                data = data[my_index+4:]
                pos = frame[1:-1].split('], [')[trap_ID]
                more_pos = pos.split(',')
                Xt.append(float(more_pos[0])-dx)
                Yt.append(float(more_pos[1])-dy)
                Zt.append(float(more_pos[2])-dz)
                ##pos = ((data.split('['))[0].split(']')[0]).split(',')
                #pos = data.split('[[')[1].split(']]')[0].split(',')
                #print(pos)
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
    #If we have multiple particles
    df = find_trajs()
    Xp = [col[1] for row,col in df.iterrows() if col[5] == ID]
    Yp = [col[2] for row,col in df.iterrows() if col[5] == ID]
    Zp = [col[3] for row,col in df.iterrows() if col[5] == ID]
    #bin data:
    bindex = 0
    spacing = 100
    Xp_plot, Xt_plot, Yp_plot, Yt_plot, Zp_plot, Zt_plot  = [], [], [], [], [], []
    for bindex in range(len(Xt)-spacing):
        Xt_plot.append(np.average(Xt[bindex:bindex+spacing+1]))
        Yt_plot.append(np.average(Yt[bindex:bindex+spacing+1]))
        Zt_plot.append(np.average(Zt[bindex:bindex+spacing+1]))
        Xp_plot.append(np.average(Xp[bindex:bindex+spacing+1]))
        Yp_plot.append(np.average(Yp[bindex:bindex+spacing+1]))
        Zp_plot.append(np.average(Zp[bindex:bindex+spacing+1]))
        bindex+=spacing+1
    #plot
    plt.plot(Xt_plot, 'r-')
    plt.plot(Yt_plot, 'b-')
    plt.plot(Zt_plot, 'g-')
    plt.plot(Xp_plot, 'r--')
    plt.plot(Yp_plot, 'b--')
    plt.plot(Zp_plot, 'g--')
    title = 'Trajectories_' + fname + ', ' + 'P-ID = ' + str(ID) + ' ' + 'T-ID = ' + str(trap_ID)
    plt.title(title)
    plt.ylabel('Position (pixels)')
    plt.xlabel('Time') #in number of frames/scaling
    plt.legend(('$x_{t}$', '$y_{t}$', '$z_{t}$', '$x_{p}$', '$y_{p}$', '$z_{p}$'))
    folder_path = path + '/trajectories/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    plt.savefig(folder_path + 'p_ID#:' + str(ID) + '_t_ID#:' + str(trap_ID) + '.png', dpi = 'figure')
    return [Xt, Xp, Yt, Yp, Zt, Zp]

if __name__ == '__main__':
    path = os.getcwd()
    plotter(0) #change the particle ID