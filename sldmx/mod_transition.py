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
	def __str__(self):
		return 'Transition(FROM: ' + str(self.oldModule) + ' TO: ' + str(self.newModule) + ')'
	def copy(self):
		print("Transition copy, NYI. how the hell would this work?")
	def restart(self):
		self.timer.restart()
	def run(self):
		if not self.timer.done():
			updatesOld = self.oldModule.run()
			updatesNew = self.newModule.run()
			updates = []
			#if len(updatesOld) != len(updatesNew) error, should this be included? :\ maybe error if on different groups
			index = 0
			time = self.timer.getDeltaNorm()
			for uO in updatesOld:
				uN = updatesNew[index]
				#c = None
				#i = None
				c = easeInOut(uO.color, uN.color, time, 1.)
				i = easeLinear(uO.intensity, uN.intensity, time, 1.)
				updates.append(Update(uO.fixId, uO.lightId, c, i))
				index += 1
		else: #Transition is done, no need to interpolate
			updates = self.newModule.run()
		
			if not self.destroy: #Just now finished, so set the replacement
				print(str(self) + " transition done")
				super(ModTransition, self).replaceWith(self.newModule)
		
		return updates

