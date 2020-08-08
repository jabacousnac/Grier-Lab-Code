# -*- coding: utf-8 -*-
# MENU: Record and Translate Trap

'''the goal is to :
1) track the trap, and record its position,
2) while recording a few frames of an experiment,
3) (OPTIONAL) give code the ability to move trap along set trajectory
4) (ONCE RECORDED) place a marker at the trap ('O' for ring trap, 'l' for line trap, 'B' for Bessel trap, and filled dot for point trap)'''

#code is adapted from MoveRecordZ
from .Task import Task
from PyQt5.QtGui import QVector3D #data type for trap.r
import numpy as np
import sys
from datetime import datetime

class RecordTrap(Task):
    """Move the trap by dragging, record its position, and take experiment"""

    def __init__(self, measure_bg=False, **kwargs):
        super(RecordTrap, self).__init__(**kwargs)
        self.traps = None
        self.measure_bg = False #set to true if we want to measure background, and write task about saving background
        self.nframe = 10 #not necessary

    def initialize(self, frame):
        self.traps = self.parent.pattern.pattern
        self.ntraps = self.traps.count()
        xc = self.parent.cgh.device.xc
        trap = self.traps.flatten()[0]
        self.r = np.array((trap.r.x(), trap.r.y()))
        self.register('Record') #record the video. To stop recording, use stop button manually

    def dotask(self):
        self.traps = self.parent.pattern.pattern
        self.ntraps = self.traps.count()
        framenum = 0 #this is the frame number we are at
        dx,dy,dz = -1.0,0.0,0.0
        dr = QVector3D(dx,dy,dz)
        #fname = str(datetime.now()) #to give a unique name to textfile
        while framenum < self.nframe: 
            self.register('Translate', traps=self.traps, dr=dr) 
            self.register('TrapLocateTest', traps=self.traps, ntraps=self.ntraps)
			#self.register('FindTraps', ntraps=self.ntraps) OTHER WAY BUT WHO KNOWS WHAT THE OUTPUT IS
            #with open(fname, 'w') as txtfile:
                #sys.stdout = txtfile
            framenum+=1
                 

