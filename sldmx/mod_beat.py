from sldmx.mod_base import Module
from sldmx.mod_group import ModGroup
#import copy

#Instantiate a new self-destructing module every beat
class ModBeat(Module):
	def __init__(self, rig, module):
		super(ModBeat, self).__init__(rig)
		self._module = module
		self.modules = ModGroup(rig)
	def __str__(self):
		return "Beat (" + str(self._module) + ")"
	def copy(self):
		return ModBeat(self.rig, self._module.copy())
	def restart(self):
		pass
	def run(self):
		if self.rig.tempo.tickedThisStep:
			newInstance = self._module.copy() #copy.copy(self._module)
			newInstance.restart()
			self.modules.add(newInstance)
			#Test for lingering module backup, maybe include auto cleanup for this later
			#print(str(self.rig.modules))
		return self.modules.run()

