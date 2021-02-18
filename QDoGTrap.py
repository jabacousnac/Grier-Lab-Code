# -*- coding: utf-8 -*-

"""QDoGTrap.py: DoG Trap"""

from .QTrap import QTrap
import numpy as np
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import (QPainterPath, QFont, QTransform)
from scipy.special import jv


class QDoGTrap(QTrap):

    def __init__(self, sigma=20, tau=10, alpha=50, **kwargs):
        super(QDoGTrap, self).__init__(alpha=alpha, **kwargs)
        self._sigma = sigma
        self._tau = tau
        self.registerProperty('sigma', tooltip=True)
        self.registerProperty('tau', tooltip=True)

    def updateStructure(self):
        kappa = 1j * np.pi / (1064*10**-9 * 10**-6) #i*pi/lambda*f
        alpha, beta = 1/(self.sigma*10**-6)**2 - kappa, 1/(self.tau*10**-6)**2 - kappa
        arg = (alpha * np.exp(-alpha * (self.cgh.qr)**2)) + \
        (beta * np.exp(-beta * (self.cgh.qr)**2))
        phi = np.exp(1j * np.arctan(arg))
        self.structure = phi


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
