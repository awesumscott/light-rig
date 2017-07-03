from sldmx.mod_base import Module
from sldmx.mod_group import ModGroup
import copy

#Instantiate a new self-destructing 
class ModBeat(Module):
	def __init__(self, rig, module):
		super(ModBeat, self).__init__(rig)
		self._module = module
		self.modules = ModGroup(rig)
	def __str__(self):
		return "Beat (" + str(self._module) + ")"
	def restart(self):
		pass
	def run(self):
		if self.rig.tempo.tickedThisStep:
			newInstance = copy.copy(self._module)
			newInstance.restart()
			self.modules.add(newInstance)
			print(str(self.rig.modules))
		return self.modules.run()

