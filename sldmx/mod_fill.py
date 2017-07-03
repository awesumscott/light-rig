from sldmx.rig_utils import Timer, Update
from sldmx.mod_base import Module

#set every light in a group with the same color/intensity
class ModFill(Module):
	#CONTROL HOOKS: fillMod.color, fillMod.intensity
	def __init__(self, rig, group, color=None, intensity=None):
		super(ModFill, self).__init__(rig)
		self.group = group
		self.color = tuple(color)
		self.intensity = intensity
	def __str__(self):
		return 'Fill (' + ('blank' if self.color == None else '#%02x%02x%02x'%self.color) + ' @ ' + ('blank' if self.intensity == None else str(int(self.intensity * 100)) + '%)');
	def run(self):
		return self.rig.group[self.group].setAll(self.color, self.intensity)

