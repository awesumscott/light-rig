from rig_utils import Update
from mod_transition import ModTransition

#module groups allow for nesting and replacing
class ModGroup(object):
	def __init__(self, rig):
		self.rig = rig
		self.modules = []
	def add(self, mod):
		self.modules.append(mod)
	def replace(self, oldModule, newModule, duration=.5):
		if not (oldModule in self.modules):
			print "Old module specified isn't in the list!"
			return
		oldModIndex = self.modules.index(oldModule)
		self.modules[oldModIndex] = ModTransition(self.rig, oldModule, newModule, duration)
	def run(self):
		newUpdates = []
		for mod in self.modules:
			newUpdates += mod.run()
					
			if mod.destroy:
				if type(mod) is ModTransition: #TODO: maybe make a standard way to do shit like this, if it'll come up more than once
					transitionModIndex = self.modules.index(mod)
					self.modules[transitionModIndex] = mod.newModule
				else:
					self.modules.remove(mod)
		return newUpdates
		