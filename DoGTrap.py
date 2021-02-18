# -*- coding: utf-8 -*-
# MENU: Add trap/DoG trap

from ..QTask import QTask
from pyfablib.traps.QDoGTrap import QDoGTrap
from PyQt5.QtGui import QVector3D


class DoGTrap(QTask):
    """Add a DoG (Difference of Gaussians) trap to the trapping pattern"""

    def __init__(self, center3=None, **kwargs):
        super(DoGTrap, self).__init__(**kwargs)
        self.center3 = center3 or (self.parent().cgh.device.xc,
                                   self.parent().cgh.device.yc,
                                   0)

    def complete(self):
        (xc, yc, zc) = self.center3
        trap = QDoGTrap(r=QVector3D(xc, yc, zc))
        self.parent().pattern.addTrap(trap)
