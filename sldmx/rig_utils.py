import math, time

#Updates are the single-frame modifiers for each light produced by each module. Updates
#can modify each other in the sequence. If an update value is set to None, it is ignored.
class Update(object): #TODO: default behavior is replace, maybe create a modify option
	def __init__(self, fixId, lightId, color, intensity, easing=None, params=None):
		self.fixId = fixId
		self.lightId = lightId
		self.color = color
		self.intensity = intensity
		self.easing = easing
		self.params = params
		
#LightSources are the positioned and weighted colors used in faders/chases
class LightSource(object):
	def __init__(self, pos, color, weight):
		self.origin = pos
		self.pos = pos
		self.color = color
		self.weight = weight

class Timer(object):
	def __init__(self, seconds):
		self.seconds = seconds
		self.start = time.clock()
		self.done = False
	def getDeltaNorm(self):
		d = (time.clock() - self.start) / self.seconds
		if d >= 1:
			self.done = True
		return d

def easeLinear(vFrom, vTo, val, vMax): #TODO: fucking fix this, this is still copied/pasted from easeInOut
	#color from/to: rgb to interpolate between
	#val/max: ratio of interpolation
	ratio = float(val) / float(vMax)
	ang = math.cos(ratio*math.pi + math.pi)/2+.5
	
	ease = lambda xFrom, xTo: float(xTo - xFrom) + xFrom
	
	if isinstance(vFrom, tuple):
		return (ease(vFrom[0], vTo[0]),
				ease(vFrom[1], vTo[1]),
				ease(vFrom[2], vTo[2]))
	return ease(vFrom, vTo)

def easeInOut(vFrom, vTo, val, vMax):
	#color from/to: rgb to interpolate between
	#val/max: ratio of interpolation
	ratio = float(val) / float(vMax)
	ang = math.cos(ratio*math.pi + math.pi)/2+.5
	
	ease = lambda ang, xFrom, xTo: int(ang * float(xTo - xFrom) + xFrom)
	
	if isinstance(vFrom, tuple):
		return (ease(ang, vFrom[0], vTo[0]),
				ease(ang, vFrom[1], vTo[1]),
				ease(ang, vFrom[2], vTo[2]))
	return ease(ang, vFrom, vTo)

#easeCircle should be used from -1 to 1
def easeCircle(vFrom, vTo, val, vMax, strength=1.):
	#strength: abruptness in hitting 100% vTo
	ratio = float(val) / float(vMax)
	halfpi = math.pi / 2
	ang = math.sin(ratio*halfpi + halfpi) * strength
	
	ease = lambda xFrom, xTo: max(min(int(ang * float(xTo - xFrom) + xFrom), 255), 0) #min(max(int(ang * float(xTo - xFrom) + xFrom), 0), 255)
	
	if isinstance(vFrom, tuple):
		return (ease(vFrom[0], vTo[0]),
				ease(vFrom[1], vTo[1]),
				ease(vFrom[2], vTo[2]))
	return ease(vFrom, vTo)
	
	