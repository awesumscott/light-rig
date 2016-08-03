#One color in list: all lights in group are that solid color
#No formula: all lights in group cycle between colors at speed
#Formula: lights in group cycle along the formula with colors moving at a pace of 1 unit/speed
#"Unit" is a vague distance approximately 15cm
#"Speed" is specified as a constructor argument

from rig_hardware import Light
from rig_utils import Update, Timer, easeInOut

class ModFader(object):
	def __init__(self, rig, group, colorListIndex, speed=2, style=0):
		self.rig = rig
		self.group = group
		self.destroy = False
		self.speed = speed		#speed = stage units per second
		
		self.colorListIndex = colorListIndex
		self.colorIndex = 0
		self.timer = Timer(speed)
		
	def run(self):
		if len(self.rig.colorList) == 0: return []
		if self.colorListIndex >= len(self.rig.colorList): self.colorListIndex = 0
		
		cl = self.rig.colorList[self.colorListIndex]
		numColors = len(cl)
		updates = []
		
		#colorIndex could be out of bounds if a shorter list is set between run calls, so check now
		if numColors <= self.colorIndex: #TODO: this might be removed if only using Transition module
			self.colorIndex = 0
		
		if numColors > 1:
			time = self.timer.getDeltaNorm()
			if time >= 1.:
				self.timer.start += self.speed #add elapsed time to restart timer without losing any ms
				self.colorIndex += 1
				time %= 1. #reset elapsed now that colorIndex is incremented, without losing ms
				if self.colorIndex >= numColors:
					self.colorIndex = 0
			
			fromC = cl[self.colorIndex]
			toC = cl[self.colorIndex+1] if self.colorIndex+1 < numColors else cl[0]
			return self.rig.group[self.group].setAll(easeInOut(fromC, toC, time, 1.), Light.IntensityBase) #using Light.IntensityBase here and below probably isn't ideal
			
		elif numColors > 0:
			return self.rig.group[self.group].setAll(cl[0], Light.IntensityBase)
		
		return []