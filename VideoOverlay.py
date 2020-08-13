import cv2
import os
import datetime
from matplotlib import pyplot as plt
import json
import re

"""Convert a video into frames, add trap positions, then convert back into a video"""
#code adapted from https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
vidcap = cv2.VideoCapture('1.avi') #change to name of file
time = datetime.datetime.now()

def getFrames(sec):
    """Convert video into frames"""
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        print(count)
        fn = str(time)[0:10] + '_t' + str(count) + '.png'
        cv2.imwrite(fn, image)
    return hasFrames

'''
sec = 0
frameRate = 1/30
count = 1
success = getFrames(sec)
while success:
	count = count + 1
	sec = sec + frameRate
	sec = round(sec, 2)
	success = getFrames(sec)
'''

def get_pos():
    """Obtain the trap positions in the form of 2D vectors, X and Y"""
    with open('2.json','r') as jsonfile: #change to actual json filename
        data = jsonfile.read()
        data = re.sub(r'\s+','',data)
        X, Y = list(), list()
        bool = True
        while bool:
            if data != '':
                pos = ((data.split('['))[1].split(']')[0]).split(',')
                X.append(float(pos[0])); Y.append(float(pos[1]));
                index = data.find(']')
                data = data[index+1:]
            else:
                bool = False
    return[X,Y]

def extension_count(extension):
    """returns the number of files found in directory with that extension"""
    myPath = os.getcwd()
    filelist = [f for f in os.listdir(myPath) if f.endswith(extension) and os.path.isfile(os.path.join(myPath,f))]
    return len(filelist)

def overlay():
    """Given the trap positions, now overlay on the frames"""
    directory = os.getcwd()
    frame = 0
    X, Y = get_pos()[0], get_pos()[1]
    if extension_count('.png') == len(X):
        bool = True
    else:
        bool = False
    print(bool)
    while bool:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('png'): #ensure that these images are the only ones with the extension
                    x,y = X[frame], Y[frame]
                    frame += 1
                    im = plt.imread(filename)
                    fig, ax = plt.subplots()
                    ax.imshow(im)
                    ax.axis('off')
                    plt.plot(x, y, 'ro')
                    plt.savefig(filename) #overwrite the existing image
    return

def stitchFrames():
    """Convert the frames into a video"""

if __name__ == '__main__':
    #getFrames(0)
    overlay()
