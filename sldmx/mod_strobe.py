from sldmx.rig_utils import Timer, Update
from sldmx.mod_base import Module

class ModStrobe(Module):
	def __init__(self, rig, group, sps=1.):
		super(ModStrobe, self).__init__(rig)
		self.group = group
		self.destroy = False
		self.sps = ((self.rig.tempo.avg)/1000) / float(sps) #strobes per beat
		self.timer = Timer(self.sps) #/2 because "one strobe" is half the time off then half the time on
		
		self.intensity = 0. #maybe this should be a parameter
		self.intensity_base = 0.
		self.intensity_max = 1.
	def __str__(self):
		return "Strobe(" + str(self.sps) + ")"
	def restart(self):
		self.timer.restart()
		self.intensity = 1.
	def run(self):
		time = self.timer.getDeltaNorm()
		#range = self.intensity_max - self.intensity_base
		
		if time <= .5:
			self.intensity = self.intensity_base
		else:
			self.intensity = self.intensity_max
		
		if self.timer.done():
			self.timer.tare(self.sps)
		
		return self.rig.group[self.group].setAll(None, self.intensity)
