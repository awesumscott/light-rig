import math, random
from sldmx.rig_hardware import Fixture
from sldmx.rig_utils import Update, Timer, easeInOut
from sldmx.mod_base import Module

#creates a TV static effect based on an intensity level
class ModStatic(Module):
	#CONTROL HOOKS: staticMod.maxIntensity
	INTERVAL = .02
	def __init__(self, rig, group, maxIntensity):
		super(ModStatic, self).__init__(rig)
		self.group = group
		self.maxIntensity = maxIntensity
		self.destroy = False
		self.timer = Timer(ModStatic.INTERVAL)
		self._newIntensity()
	def __str__(self):
		return 'Static'
	def restart(self):
		pass
		#self.timer.restart()
	def _newIntensity(self):
		self.intensity = random.random() * self.maxIntensity
	def run(self):
		time = self.timer.getDeltaNorm()
		
		if self.timer.done():
			self.timer.tare(ModStatic.INTERVAL)
			
			#new random intensity, possibly favoring higher end
			#20% variation = maxIntensity - (maxIntensity * .02 * random)
			self._newIntensity()
		
		return self.rig.group[self.group].setAll(None, self.intensity)
