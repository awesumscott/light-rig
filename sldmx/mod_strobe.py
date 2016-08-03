from rig_utils import Timer, Update

class ModStrobe(object):
	def __init__(self, rig, group, sps=1.):
		self.rig = rig
		self.group = group
		self.destroy = False
		self.sps = sps #strobes per second
		self.timer = Timer(1./sps) #/2 because "one strobe" is half the time off then half the time on
		
		self.intensity = 1. #maybe this should be a parameter
		self.intensity_base = 0.
		self.intensity_max = 1.
	
	def run(self):
		time = self.timer.getDeltaNorm()
		if time <= .5:
			self.intensity = self.intensity_base
		else:
			self.intensity = self.intensity_max
		self.intensity %= 1.
		
		return self.rig.group[self.group].setAll(None, self.intensity)