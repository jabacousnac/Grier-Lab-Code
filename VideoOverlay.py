import cv2
import os
import datetime
from matplotlib import pyplot as plt

"""Convert a video into frames, add trap positions, then convert back into a video"""
#code adapted from https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
vidcap = cv2.VideoCapture('bird.avi') #change to name of file
time = datetime.datetime.now()

def getFrames(sec):
    """Convert video into frames"""
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
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

def overlay():
    """Given the trap positions, now overlay on the frames"""
    directory = os.getcwd()
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('png'): #ensure that this is the only file of that filetype
                X = plt.imread(filename)
                fig, ax = plt.subplots()
                ax.imshow(X)
                ax.axis('off')
                plt.plot(X,Y,'ro')
                plt.show()
    return

def stitchFrames():
    """Convert the frames into a video"""

if __name__ == '__main__':
    modifyFrames()
    #getFrames(0)