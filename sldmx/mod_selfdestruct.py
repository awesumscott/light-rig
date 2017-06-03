from sldmx.rig_utils import Timer, Update
from sldmx.mod_base import Module

#run specified modules, but stop and remove self after specified time
class ModSelfDestruct(Module):
	def __init__(self, rig, module, duration):
		super(ModSelfDestruct, self).__init__(rig)
		self.module = module
		self.timer = Timer(duration)
	def restart(self):
		self.timer.restart()
		self.module.restart()
	def run(self):
		if not self.timer.done():
			return self.module.run()
		self.destroy = True
		return []