from sldmx.rig_utils import Update, Timer, easeLinear, easeInOut
from sldmx.mod_base import Module

class ModTransition(Module):
	def __init__(self, rig, oldModule, newModule, duration=.5):
		super(ModTransition, self).__init__(rig)
		self.oldModule = oldModule
		self.newModule = newModule
		self.destroy = False
		self.duration = duration
		self.timer = Timer(duration)
	def restart(self):
		self.timer.restart()
	def run(self):
		updatesOld = self.oldModule.run()
		updatesNew = self.newModule.run()
		updates = []
		#if len(updatesOld) != len(updatesNew) error, should this be included? :\ maybe error if on different groups
		index = 0
		time = self.timer.getDeltaNorm()
		for uO in updatesOld:
			uN = updatesNew[index]
			c = None
			i = None
			#TODO: in the future this should make sure both modules match
			if uO.color != None:
				c = easeInOut(uO.color, uN.color, time, 1.)
			if uO.intensity != None:
				i = easeLinear(uO.intensity, uN.intensity, time, 1.)
			updates.append(Update(uO.fixId, uO.lightId, c, i))
			index += 1
		
		if self.timer.done():
			print("transition done")
			super(ModTransition, self).replaceWith(self.newModule)
		
		return updates