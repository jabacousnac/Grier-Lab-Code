import json
import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import os

def particle_getter():
    fname = '2020-09-09--17-32-45'
    frames, coords = [], []
    framenum = 1
    with open('your_MLpreds_' + fname + '.json', 'r') as myFile:
        myList = json.load(myFile)  # pred_list is a list containing dictionaries. Each dict has x_p, y_p, z_p, etc.
        for PreDict in myList:
            frames.append(PreDict['framenum'])
            myframe = int(PreDict['framenum'])
            if myframe == framenum: #do it only for this frame
                coords.append([int(PreDict['x_p']), int(PreDict['y_p']), int(PreDict['z_p'])])
    fn = 'image0001.png'
    path = os.getcwd()
    img = cv.imwrite(path + '/' + fn, 0)
    print(coords)
    for part in coords:
        img = cv.circle(cv.imwrite(fn,img), (part[0], part[1]),5,(0,255,0),-1)
    cv.imshow('image',img)
    cv.waitKey(0)

if __name__ == '__main__':
    particle_getter()
