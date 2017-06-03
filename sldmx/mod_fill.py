from sldmx.rig_utils import Timer, Update
from sldmx.mod_base import Module

#set every light in a group with the same color/intensity
class ModFill(Module):
	def __init__(self, rig, group, color=None, intensity=None):
		super(ModFill, self).__init__(rig)
		self.group = group
		self.color = color
		self.intensity = intensity
	def run(self):
		return self.rig.group[self.group].setAll(self.color, self.intensity)