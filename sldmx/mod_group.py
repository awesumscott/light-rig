from rig_utils import Update
from mod_transition import ModTransition

#module groups allow for nesting and replacing
class ModGroup(object):
	def __init__(self, rig):
		self.rig = rig
		self.modules = []
	#def add(self, mod):
	#	self.modules.append(mod)
	def add(self, modClass, *params):
		mod = modClass(self.rig, *params)
		self.modules.append(mod)
		return mod
	#def replace(self, oldModule, newModule, duration=.5):
	#	if not (oldModule in self.modules):
	#		print "Old module specified isn't in the list!"
	#		return
	#	oldModIndex = self.modules.index(oldModule)
	#	self.modules[oldModIndex] = ModTransition(self.rig, oldModule, newModule, duration)
	def run(self):
		newUpdates = []
		for mod in self.modules:
			newUpdates += mod.run()
			
			if mod.destroy:
				if mod.replacement == None:
					self.modules.remove(mod)
				else:
					self.modules[self.modules.index(mod)] = mod.replacement
		return newUpdates
		