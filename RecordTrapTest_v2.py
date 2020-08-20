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
        self.nframes = 300                     #### Declare whatever you can in __init__ and only declare what you use
        self.dr = QVector3D(0.5, 0.5, 0.)
  
        time = dt.datetime.now()                #### It's best practice to avoid using global variables, if possible
        self.fname = str(time)[:-7]
        self.output = []                        #### Place to store the output

        
#### If you declare traps in initialize(), you'll get the traps on screen when the task runs, rather than when the task is registered.       
    def initialize(self, frame):
        self.dvr = self.parent.dvr              #### This is ugly, but it should work
        if self.fname is not None:
            self.dvr.filename = 'pyfab.avi'
        self.dvr.recordButton.animateClick()

    def doprocess(self, frame):
        traps = self.parent.pattern.pattern  
        if traps.count() > 0:                   #### Just take first trap    
            trap = traps.flatten()[0]
#             sym = trap.plotSymbol() #no worries, we'll use this info later
            coord = ((trap.r.x(), trap.r.y(), trap.r.z())) 
            self.output.append(coord)
            trap.moveBy(self.dr)
        else:
            print('Error: no traps to translate!')  #### If there aren't any traps on screen, abort
            self.output.append(None)        
            
    def doTask(self):
        self.dvr.stopButton.animateClick()
        print(self.fname)
        with open('pyfab.json', 'w') as myfile:
            json.dump(np.array(self.output), myfile)
        
            
