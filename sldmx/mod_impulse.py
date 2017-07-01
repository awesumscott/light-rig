from sldmx.rig_utils import Update
from sldmx.mod_base import Module
from sldmx.rig_utils import Timer, easeOutFast

class ModImpulse(Module):
	def __init__(self, rig, group, duration=1.):
		super(ModImpulse, self).__init__(rig)
		self.group = group
		self.destroy = False
		
		#self.intensity = 1. #maybe this should be a parameter
		self.timer = Timer(self.rig.tempo.avg / 1000)
	def __str__(self):
		return "Impulse"
	def restart(self):
		self.timer.restart()
		self.intensity = 1.
	def run(self):
		if self.timer.done():
			self.destroy = True
		return self.rig.group[self.group].setAll(None, easeOut(1., 0., self.timer.getDeltaNorm()))

