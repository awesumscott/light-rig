from sldmx.rig_utils import Update
from sldmx.mod_base import Module
from sldmx.mod_transition import ModTransition

#module groups allow for nesting and replacing
class ModGroup(Module):
	def __init__(self, rig):
		super(ModGroup, self).__init__(rig)
		self._modules = []
	def __len__(self):
		return len(self._modules)
	def __getitem__(self,index):
		return self._modules[index]
	def add(self, mod):
		self._modules.append(mod)
	def pop(self):
		if len(self):
			self._modules.pop()
	#def add(self, modClass, *params):
	#	mod = modClass(self.rig, *params)
	#	self.modules.append(mod)
	#	return mod
	#def replace(self, oldModule, newModule, duration=.5):
	#	if not (oldModule in self.modules):
	#		print "Old module specified isn't in the list!"
	#		return
	#	oldModIndex = self.modules.index(oldModule)
	#	self.modules[oldModIndex] = ModTransition(self.rig, oldModule, newModule, duration)
	def run(self):
		newUpdates = []
		for mod in self._modules:
			newUpdates += mod.run()
		
		for mod in self._modules:
			if mod.destroy:
				if mod.replacement == None:
					self._modules.remove(mod)
				else:
					self._modules[self._modules.index(mod)] = mod.replacement
		return newUpdates
		