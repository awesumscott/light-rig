from rig_utils import Update

#TODO: make this use a duration and an easing equation
#y=cos(.5pi*x+.5pi)+1
#or y=(x-1)^2
class ModImpulse(object):
	def __init__(self, rig, group, duration=1.):
		self.rig = rig
		self.group = group
		self.destroy = False
		
		self.intensity = 1. #maybe this should be a parameter
		self.intensity_base = .2 #baseline intensity for pulses to stop at
		self.intensity_decel = .96 #ratio at which to decelerate intensity each frame
	
	def run(self):
		if self.intensity > self.intensity_base: #mid-pulse
			ni = self.intensity * self.intensity_decel
			self.intensity = ni
		else:
			self.destroy = True
		
		return self.rig.group[self.group].setAll(None, self.intensity)