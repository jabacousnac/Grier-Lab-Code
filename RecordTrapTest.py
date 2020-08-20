# -*- coding: utf-8 -*-
# MENU: Record and Translate Trap

from .Task import Task
from PyQt5.QtGui import QVector3D
import numpy as np
import json
import datetime as dt


class RecordTrapTest(Task):
    """Translate trap, record and save its position in JSON file, while recording"""

    def __init__(self, **kwargs):
        super(RecordTrapTest, self).__init__(**kwargs)
        self.nframes = 500                     
        self.dr = QVector3D(0.5, 0.5, 0.)
    
    def initialize(self, frame):
        time = dt.datetime.now()               
        self.dvr = self.parent.dvr             
        self.dvr.filename = str(time)[:10] + '.avi'
        self.dvr.recordButton.animateClick()
        self.time = time

    def doprocess(self, frame): #use self.dvr._framenumber to obtain the frame at which we're at
        traps = self.parent.pattern.pattern
        if traps.count() > 0:                   
            trap = traps.flatten()[0]
            coord = ((trap.r.x(), trap.r.y(), trap.r.z())) 
            trap.moveBy(self.dr)
            with open(str(self.time)[:10] + '--' + str(self.time)[11:-7] + '.json', 'a') as myfile:
                json.dump(coord, myfile)
        else:
            print('Error: no traps to translate!') 
            coord = None
        
            
