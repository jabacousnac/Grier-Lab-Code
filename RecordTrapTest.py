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

    def dotask(self):
        self.traps = self.parent.pattern.pattern
        self.ntraps = self.traps.count()
        dx, dy, dz, framenum = 0.5, 0.0, 0.0, 0
        self.nframes = 500
        dr = QVector3D(dx,dy,dz)
        self.register('Record', fn = fname + '.avi', stop = False)
        while framenum < self.nframes:
            self.register('Translate', traps=self.traps, dr=dr)
            self.register('TrapLocateTest', fn=fname, traps=self.traps, ntraps=self.ntraps)
            framenum += 1


                 

