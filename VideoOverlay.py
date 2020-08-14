import cv2
import os
import datetime
from matplotlib import pyplot as plt
import json
import re

"""Convert a video into frames, add trap positions, then convert back into a video"""
#code adapted from https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
vidname = '2.avi'
vidcap = cv2.VideoCapture(vidname) #change to name of file
time = datetime.datetime.now()

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
    return [X,Y]

def getFrames(sec):
    """Convert video into frames"""
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        if count % 50 == 0:
            print(count)
        fn = str(time)[0:10] + '_t' + str(count) + '.png'
        cv2.imwrite(fn, image)
    return hasFrames

def extension_count(extension):
    """returns the number of files found in directory with that extension"""
    myPath = os.getcwd()
    filelist = [f for f in os.listdir(myPath) if f.endswith(extension) and os.path.isfile(os.path.join(myPath,f))]
    return len(filelist)

def overlay():
    """Given the trap positions, now overlay on the frames"""
    directory = os.getcwd()
    frame, imageList = 0, list()
    X, Y = get_pos()[0], get_pos()[1]
    while frame < len(X):
        for root, dirs, files in os.walk(directory):
            for filename in files:
                fn = str(time)[0:10] + '_t' + str(frame + 1) + '.png'
                if filename == fn: #ensure that these images are the only ones with the extension .png
                    imageList.append(filename)
                    print(frame)
                    x,y = X[frame], Y[frame]
                    frame += 1
                    im = plt.imread(filename)
                    fig, ax = plt.subplots()
                    ax.imshow(im)
                    ax.axis('off')
                    plt.plot(x, y, 'ro')
                    plt.savefig(filename) #overwrite the existing image
                    plt.close('all')
    return imageList

def stitchFrames():
    """Convert the frames into a video, and delete all .png files"""
    directory = os.getcwd()
    images = overlay() #this is where we make function call to overlay
    frame = cv2.imread(os.path.join(directory, images[0]))
    height, width, layers = frame.shape
    vid = cv2.VideoWriter(vidname, 0, 1, (width, height))
    for image in images:
        print(image)
        vid.write(cv2.imread(os.path.join(directory, image)))
        os.remote(os.path.join(directory, image))
    cv2.destroyAllWindows()
    vid.release()


if __name__ == '__main__':
    #First create the frames
    sec = 0
    frameRate = 1 / 12.5
    count = 1
    success = getFrames(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrames(sec)
    """Overlay, then stitch"""
    stitchFrames()
    print(datetime.datetime.now() - time)