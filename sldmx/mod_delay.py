from sldmx.rig_utils import Timer, Update
from sldmx.mod_base import Module

class ModDelay(Module):
	def __init__(self, rig, module, duration):
		super(ModDelay, self).__init__(rig)
		self.module = module
		self.timer = Timer(duration)
	def restart(self):
		self.timer.restart()
	def run(self):
		if not self.timer.done():
			return []
		super(ModDelay, self).replaceWith(self.module)
		self.module.restart()
		return self.module.run()