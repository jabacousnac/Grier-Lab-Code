import os
import json
import pandas as pd
from pandas import DataFrame, Series
#import numpy as np
import trackpy as tp
from matplotlib import pyplot as plt
import cv2 as cv #apparently, it needs to be commented out for Plot Trajectories to work

def get_partDict():
    #obtain a dictionary of form {framenumber: [p1, p2, p3, ...]}, where p's are particle coordinates
    frames, param, partDict = [], [], {}
    framenum = 1
    with open('your_MLpreds.json', 'r') as myFile:
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
    thresh = [300, 300, 300, 2]
    t = tp.link_df(df, thresh, memory = 40, pos_columns = ['x', 'y', 'z', 'a'], t_column = 't');
    pd.set_option('display.max_rows', None , 'display.max_columns', None)
    #t1 = tp.filter(t, condition)
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
    print([T,X])
    plt.figure()
    plt.plot(T, X, 'b-')
    plt.show()

def test_plot(frame, ID): #ID is a string of form ####
    #pull up a normalized picture and identify which particle corresponds to the one labeled by the ID
    impath = path + '/norm_images/image' + frame + '.png'
    im = cv.imread(impath)
    df = find_trajs()
    for row, col in df.iterrows():
        if int(col[0]) == int(frame) and int(col[5]) == ID:
            coord = (int(col[1]), int(col[2]))
    im = cv.circle(im, (coord[0], coord[1]), 5 , (0,255,0), -1)
    cv.imshow('image', im)
    cv.waitKey(0)
    cv.destroyAllWindows()

def pull_up_IDs(frame): #frame is a string ####
    #provide a frame number, and it will display the image with the particle IDs
    impath = path + '/norm_images/image' + frame + '.png'
    im = cv.imread(impath)
    df = find_trajs()
    font = cv.FONT_HERSHEY_SIMPLEX
    for row, col in df.iterrows():
        if int(col[0]) == int(frame):
            marker = col[5]
            im = cv.putText(im, str(int(col[5])), (int(col[1]), int(col[2])), font, 1, (0,0,0), 2, cv.LINE_AA)
    cv.imshow('image', im)
    cv.imwrite(path + '/particle_IDs/' + frame + '.png', im)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    path = os.getcwd()
    pull_up_IDs('1111')