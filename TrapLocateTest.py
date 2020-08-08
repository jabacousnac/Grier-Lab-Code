from .Task import Task
from PyQt5.QtGui import QVector3D #data type for trap.r
import numpy as np

class TrapLocateTest(Task):
	"""Obtain the coordinates of where the trap currently is"""

	def __init__(self, traps=None, ntraps=None, **kwargs):
		super(TrapLocateTest, self).__init__(**kwargs)
		self.traps = None
		self.ntraps = ntraps
	
	def dotask(self):
		self.traps = self.parent.pattern.pattern
		self.ntraps = self.traps.count()
		coord = list() 
		if self.ntraps > 0:
			for trap in self.traps.flatten():
				sym = trap.plotSymbol()
				coord.append((trap.r.x(), trap.r.y(), trap.r.z()))
		print(coord) #coord is a list containing (x,y,z) for all traps in one frame
		return
