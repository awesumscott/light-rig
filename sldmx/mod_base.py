from rig_utils import Update

#module groups allow for nesting and replacing
class Module(object):
	def __init__(self, rig):
		self.rig = rig
		self.destroy = False
		self.replacement = None
	def restart(self):
		pass
	def replaceWith(self, newModule):
		self.destroy = True
		self.replacement = newModule
	def run(self):
		return []
		