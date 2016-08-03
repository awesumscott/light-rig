import math
from rig_hardware import Fixture
from rig_utils import Update, Timer, easeInOut

class ModChase(object):
	def __init__(self, rig, group, lightSources, type, speed=1., slope=1.):
		self.rig = rig
		self.group = group
		self.lightSource = lightSources
		self.type = type
		self.slope = slope
		self.speed = speed
		self.destroy = False
		self.dir = speed / abs(speed)
		self.timer = Timer(1)
		self.startpoint = 0
		
		#find endmost position according to direction + distance right outside it according to speed
		rect = self.rig.group[self.group].rect
		if speed > 0:
			for ls in self.lightSource:
				ls.origin = rect[0] - ls.pos - ls.weight
				self.endpoint = rect[2]
		else:
			for ls in self.lightSource:
				ls.origin = rect[2] + ls.pos + ls.weight
				self.endpoint = rect[0]
		
	def run(self):
		time = self.timer.getDeltaNorm()
		
		for ls in self.lightSource:
			ls.pos = ls.origin + time / self.speed
		
		updates = self.rig.group[self.group].interp(self.lightSource, Fixture.InterpLinear, self.speed)
		
		lastLight = self.lightSource[-1]
		self.destroy = (self.dir == 1. and lastLight.pos > self.endpoint + lastLight.weight) or (self.dir == -1. and lastLight.pos < self.endpoint - lastLight.weight)
		
		return updates