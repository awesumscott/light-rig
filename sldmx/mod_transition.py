from rig_utils import Update, Timer, easeLinear, easeInOut

class ModTransition(object):
	def __init__(self, rig, oldModule, newModule, duration=.5):
		self.rig = rig
		self.oldModule = oldModule
		self.newModule = newModule
		self.destroy = False
		self.duration = duration
		self.timer = Timer(duration)
	
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
		
		if self.timer.done:
			print "transition done"
			self.destroy = True
		
		return updates