from .Task import Task
from PyQt5.QtGui import QVector3D #data type for trap.r
import numpy as np
import json
import os.path
from os import path

class TrapLocateTest(Task):
	"""Obtain the coordinates of where the trap currently is and saves to a .json file"""

	def __init__(self, traps=None, ntraps=None, **kwargs):
		super(TrapLocateTest, self).__init__(**kwargs)
		self.traps = None
		self.ntraps = ntraps
	
	def dotask(self):
		self.traps = self.parent.pattern.pattern
		self.ntraps = self.traps.count()
		fname = 'mysillyexperiment' + '.json' #change this
		if self.ntraps > 0:
			for trap in self.traps.flatten():
				sym = trap.plotSymbol() #no worries, we'll use this info later
				coord = ((sym, trap.r.x(), trap.r.y(), trap.r.z())) 
			print(coord)
			with open(fname, 'a') as myfile:
					json.dump(coord, myfile)
