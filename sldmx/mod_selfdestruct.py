from rig_utils import Timer, Update
from mod_base import Module

class ModSelfDestruct(Module):
	def __init__(self, rig, module, duration):
		super(ModSelfDestruct, self).__init__(rig)
		self.module = module
		self.timer = Timer(duration)
		self.destroy = False
	def restart(self):
		self.timer.restart()
		self.module.restart()
	def run(self):
		if not self.timer.done():
			return self.module.run()
		self.destroy = True
		return []