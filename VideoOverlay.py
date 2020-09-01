import cv2 as cv
import os
import datetime
import json
import re

"""Convert a video into frames, add trap positions, then convert back into a video"""
#part of code adapted from https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
fname = '2020-08-20--16_51_30' #change to name of file
vidcap = cv.VideoCapture(fname + '.avi')
time = datetime.datetime.now()
fps = 30 #change accordingly

def get_pos():
    """Obtain the trap positions in the form of 2D vectors, X and Y"""
    with open(fname + '.json','r') as jsonfile: #change to actual json filename
        data = jsonfile.read()
        data = re.sub(r'\s+','',data)
        X, Y = [], [] #### works faster than list()
        bool = True
        while bool:
            if data != '':
                pos = ((data.split('['))[1].split(']')[0]).split(',')
                X.append(float(pos[0]))
                Y.append(float(pos[1]))
                index = data.find(']')
                data = data[index+1:]
            else:
                bool = False
    return [X, Y]

def getFrames(sec):
    """Convert video into frames"""
    vidcap.set(c.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    radius, color, thickness = 5, (0,255,0), -1 #change for ring trap
    if hasFrames and count < len(X):
        fn = str(time)[0:10] + '_t' + str(count+1) + '.png'
        print(fn)
        imageList.append(fn)
        img = cv.circle(cv.imwrite(fn, image), (X[count],Y[count]), radius, color, thickness)
        cv.imwrite(fn, img)
    else:
        return [False, imageList]
    return [hasFrames, imageList]

def extension_count(extension):
    """returns the number of files found in directory with that extension"""
    myPath = os.getcwd()
    filelist = [f for f in os.listdir(myPath) if f.endswith(extension) and os.path.isfile(os.path.join(myPath,f))]
    return len(filelist)

def stitchFrames():
    """Convert the frames into a video"""
    directory = os.getcwd()
    images = getFrames(sec)[1]
    frame = cv.imread(os.path.join(directory, images[0]))
    height, width, layers = frame.shape
    vid = cv.VideoWriter(fname + '.avi', 0, fps, (width, height))
    for image in images:
        print(image)
        vid.write(cv.imread(os.path.join(directory, image)))
        #os.remove(os.path.join(directory, image)) #unexpected consequences!
    cv.destroyAllWindows()
    vid.release()
    print(datetime.datetime.now() - time) #to know how long it takes to run this file

if __name__ == '__main__':
    """First create the frames"""
    sec = 0
    frameRate = 1/fps
    count = 0
    X,Y, imageList = get_pos()[0], get_pos()[1], []
    success = getFrames(sec)[0]
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrames(sec)[0]
    """Overlay, then stitch"""
    stitchFrames()
