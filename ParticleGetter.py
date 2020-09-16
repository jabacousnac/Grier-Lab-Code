import json
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import trackpy as tp
from matplotlib import pyplot as plt

def get_partDict():
    #obtain a dictionary of form {framenumber: [p1, p2, p3, ...]}, where p's are particle coordinates
    frames, param = [], []
    framenum = 1
    with open('experiments_refined.json', 'r') as myFile:
        myList = json.load(myFile)  # pred_list is a list containing dictionaries.
            # Each dict has x_p, y_p, z_p, etc.
        for PreDict in myList:
            frame = PreDict['framenum']
            param = (PreDict['x_p'], PreDict['y_p'], PreDict['z_p'], PreDict['a_p'])
            if frame in partDict:
                partDict[frame].append(param)
            else:
                partDict[frame] = [param]
    return partDict

def find_trajs():
    #find the trajectories of particles across an experiment
    partDict = get_partDict()
    time_list, x_list, y_list, z_list, a_list = [], [], [], [], []
    for time in partDict:
        param = partDict[time]
        for particle in param:
            time_list.append(time)
            x_list.append(particle[0])
            y_list.append(particle[1])
            z_list.append(particle[2])
            a_list.append(particle[3])
    df = DataFrame(time_list, columns = ['t'])
    df.insert(1, 'x', x_list, True)
    df.insert(2, 'y', y_list, True)
    df.insert(3, 'z', z_list, True)
    df.insert(4, 'a', a_list, True)
    thresh = [700, 700, 700, 1]
    t = tp.link_df(df, thresh, memory = 5, pos_columns = ['x', 'y', 'z', 'a'], t_column = 't');
    pd.set_option('display.max_rows', None , 'display.max_columns', None)
    #t1 = tp.filter(t, condition)
    #print (t['particle'])
    print(t)
    return t

def traj_ID(ID):
    #follow a particle through the experiment
    X, T = [], []
    df = find_trajs()
    for row, col in df.iterrows():
        if col[5] == ID:
            X.append(col[1])
            T.append(col[0])
    print([len(X), len(T)])
    plt.figure()
    plt.plot(T, X, 'b-')
    plt.show()


if __name__ == '__main__':
    partDict = {} #{framenumber: (x1,y1,z1), (x2,y2,z2), ...} since keys have to be unique
    traj_ID(1)