# -*- coding: utf-8 -*-
# MENU: Record and Translate Trap

from .Task import Task
from PyQt5.QtGui import QVector3D
import numpy as np
import datetime as dt

time = dt.datetime.now()
fname = str(time)[:-7]

class RecordTrapTest(Task):
    """Translate trap, record and save its position in JSON file, while recording"""

    def __init__(self, measure_bg=False, **kwargs):
        super(RecordTrapTest, self).__init__(**kwargs)
        self.traps = None
        self.measure_bg = False 
        self.nframes = 1000

    def initialize(self, frame):
        self.traps = self.parent.pattern.pattern
        self.ntraps = self.traps.count()
        xc = self.parent.cgh.device.xc
        trap = self.traps.flatten()[0]
        self.r = np.array((trap.r.x(), trap.r.y()))
        self.framenum = 0
        self.register('Record', fn = fname + '.avi', stop = True, nframes = self.nframes)

    def dotask(self):
        dx, dy, dz = 0.2, 0.0, 0.0
        dr = QVector3D(dx,dy,dz)
        if self.framenum < self.nframes:
            self.register('Translate', traps=self.traps, dr=dr)
            self.register('TrapLocateTest', fn=fname, traps=self.traps, ntraps=self.ntraps)
            self.framenum += 1



                 

