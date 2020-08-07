# -*- coding: utf-8 -*-

'''the goal is to :
1) track the trap, and record its position,
2) while recording a few frames of an experiment,
3) (OPTIONAL) give code the ability to move trap along set trajectory
4) (ONCE RECORDED) place a marker at the trap ('O' for ring trap, 'l' for line trap, 'B' for Bessel trap, and filled dot for point trap)'''

#code is adapted from MoveRecordZ
from .Task import Task
from PyQt5.QtGui import QVector3D #data type for trap.r
import numpy as np

class MoveRecordTrap(Task):
    """Move the trap by dragging, record its position, and take experiment"""

    def __init__(self, measure_bg=False, **kwargs):
        super(MoveRecordTrap, self).__init__(**kwargs)
        self.Traps = None
        self.measure_bg = False #set to true if we want to measure background, and write task about saving background
        self.nframe = 50

    def initialize(self, frame):
        self.traps = self.parent.pattern.pattern
        xc = self.parent.cgh.device.xc
        trap = self.traps.flatten()[0]
        self.r = np.array(trap.r.x(), trap.r.y())
        self.register('record') #record the video. To stop recording, use stop button manually

    def dotask(self):
        self.traps = self.parent.pattern.pattern
        dx,dy,dz = -10.0,0.0,0.0
        dr = QVector3D(dx,dy,dz)
        self.register('Translate', trap=self.traps, dr=dr) #remove 'Translate" and see if mouse drag is possible while recording trap position
        for trap in traps.flatten():
            coord = (trap.r.x(), trap.r.y(), trap.r.z())
            print(coord)