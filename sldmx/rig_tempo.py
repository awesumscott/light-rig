import time

#60000/bpm = bms
#60000/bms=bpm
class TapTempo(object):
	_THRESHOLD = .1 #percentage difference from last set average to warrant emptying data
	def __init__(self):
		self.tick = False
		self._cur = 0
		self._last = 0
		self._times = []
		self.avg = 1000 #default 1 second
		
		self._lastTick = TapTempo._getTicks()
		self._nextTick = self._lastTick + self.avg
		self._curDelta = 0
		self.tickedThisStep = True
	
	@staticmethod
	def _getTicks():
		return int(round(time.time() * 1000))
	def step(self):
		cur = self._getTicks()
		diff = cur - self._lastTick
		self.tickedThisStep = False
		
		if diff > self.avg:
			self.tickedThisStep = True
			#print("tick " + str(diff))
			self._lastTick += diff
			diff %= self.avg
		self._curDelta = diff
		
	def getDelta(self):
		#I could maybe calculate a new up-to-date diff here,
		#as long as I cap it at the max (avg) so it doesn't
		#mess up module calculations
		return self._curDelta / self.avg
		
	def tap(self):
		cur = TapTempo._getTicks()
		if self._last == 0:
			pass
		else:
			span = cur - self._last
			if abs(span - self.avg) > self.avg * TapTempo._THRESHOLD:
				#start over
				print("started over")
				self.avg = span
				self._times = [span]
			else:
				#update average
				self._times.append(span)
				self.avg = float(sum(self._times)) / max(len(self._times), 1)
			
				
			
			print(str(self.avg))
		self._last = cur
	
	def update(self):
		self.tick = False
		#if time hit <= this tick, set
		self.tick = True
