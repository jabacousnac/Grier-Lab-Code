# -*- coding: utf-8 -*-

"""QDoGTrap.py: DoG Trap"""

from .QTrap import QTrap
import numpy as np
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import (QPainterPath, QFont, QTransform)
#import sys
#np.set_printoptions(threshold=sys.maxsize)


class QDoGTrap(QTrap):

    def __init__(self, sigma=40, tau=20, alpha=50, **kwargs):
        super(QDoGTrap, self).__init__(alpha=alpha, **kwargs)
        self._sigma = sigma
        self._tau = tau
        self.registerProperty('sigma', tooltip=True)
        self.registerProperty('tau', tooltip=True)

    def updateStructure(self):
        wavelength = 1064e-9/48e-9
        z = 1e-6/48e-9
        q = 2 * np.pi * 1.49 / wavelength
        kappa = 1j * np.pi /(wavelength * z)
        u = np.exp((kappa * self.cgh.qr / q * self.sigma)**2) - np.exp((kappa * self.cgh.qr / q * self.tau)**2)
        phi = np.angle(np.sin(u) / (np.cos(u)-1))
        self.structure = np.exp(1j * phi) * u

    def plotSymbol(self):
        sym = QPainterPath()
        font = QFont('Sans Serif', 10, QFont.Black)
        sym.addText(0, 0, font, 'D')
        # Scale symbol to unit square
        box = sym.boundingRect()
        scale = 1./max(box.width(), box.height())
        tr = QTransform().scale(scale, scale)
        # Center symbol on (0, 0)
        tr.translate(-box.x() - box.width()/2., -box.y() - box.height()/2.)
        return tr.map(sym)

    @pyqtProperty(float)
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, sigma):
        self._sigma = sigma
        self.updateStructure()

    @pyqtProperty(int)
    def tau(self):
        return self._tau

    @tau.setter
    def tau(self, tau):
        self._tau = tau
        self.updateStructure()
