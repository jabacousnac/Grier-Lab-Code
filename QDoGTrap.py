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
#1. real units -> pixels
        wavelength = 1064e-9 / (48e-9)
        z = 1e-7 / (48e-9)
#2. kappa, a, b are quantities to simplify calculations
        kappa = 1j * np.pi /(wavelength * z)
        a, b = 1/(self.sigma)**2 - kappa, 1/(self.tau)**2 - kappa
#3. get phase part
        arg = (a * np.exp(-a * (self.cgh.qr)**2)) - \
        (b * np.exp(-b * (self.cgh.qr)**2))
#4. get amplitude part
        u = -kappa * np.exp((1j * 2*np.pi/wavelength * z) + kappa * (self.cgh.qr)**2) * \
        (1/a * np.exp(kappa**2 * (self.cgh.qr)**2 / a) - 1/b * np.exp(kappa**2 * (self.cgh.qr)**2 / b))
        self.structure = np.exp(1j * np.angle(arg)) * u
        print (np.exp(1j * np.angle(arg)) * u)


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
