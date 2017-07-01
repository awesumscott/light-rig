from sldmx.rig_utils import Update, easeCircle

#Fixtures represent the actual hardware units with one or multiple light sections
class Fixture(object):
	InterpLinear = 1 #TODO: maybe these should go in an interp helper class?
	InterpRadial = 2
	def __init__(self, id, channels, universe, posX, posY, fixedchannels):
		self.universe = universe #TODO: add this stuff in later, assemble em all via universe and send
		self.id = id
		self.light = []
		self.channels = channels
		self.channelOffset = 0
		self.posX = posX
		self.posY = posY
		self.fixedchannels = fixedchannels
		self.rect = None #(xMin, yMin, xMax, yMax)
	def __repr__(self):
		return "Fixture ID " + str(self.id) + " on DMX channel " + str(self.channelOffset + 1) + "\n"
	def addLight(self, light):
		self.light.append(light)
		if self.rect == None:
			self.rect = (light.posX, light.posY, light.posX, light.posY)
		else:
			self.rect = (min(self.rect[0], light.posX), min(self.rect[1], light.posY), max(self.rect[2], light.posX), max(self.rect[3], light.posY))
	def setAll(self, color=None, intensity=None):
		updates = []
		i = 0
		for i in range(len(self.light)):
			updates.append(Update(self.id, i, color, intensity))
			i += 1
		return updates
	def interp(self, lightSource, type, speed):
		#lightSource: array of LightSource objects
		#type: linear, radial
		i = 0
		updates = []
		dir = speed / abs(speed)
		if type == Fixture.InterpLinear:
			for light in self.light:
				for ls in lightSource:
					dist = light.posX - ls.pos
					if abs(dist) <= ls.weight:
						updates.append(Update(self.id, i, ls.color, None, easeCircle, [dist, ls.weight, ls.weight]))
				i += 1
		elif type == Fixture.InterpRadial:
			for light in self.light:
				for ls in lightSource:
					#((self.rect[0] - self.rect[2])**2 + (self.rect[1] - self.rect[3])**2)**.5
					#val = group center dist to light center, vmax = ls.pos
					updates.append(Update(self.id, i, ls.color, None))
				i += 1
		return updates
	
	def output(self):
		channels = [0] * self.channels
		for light in self.light:
			start = light.rgbOffset
			channels[start:start + 3] = light.output()
		for fc in self.fixedchannels:
			channels[int(fc)] = self.fixedchannels[fc]
		return channels

#Lights are the individually controllable sections within a fixture
class Light(object):
	IntensityBase = .5
	def __init__(self, rgbOffset, posX, posY):
		self.rgbOffset = rgbOffset
		self.posX = posX
		self.posY = posY
		self.color = (0, 0, 0)
		self.intensity = .5
	def output(self):
		#intensity = self.intensity if self.intensity != None else Light.IntensityBase
		intensity = self.intensity
		
		#print(str(intensity))
		return tuple(int(intensity * c) for c in self.color)

#Groups of fixtures can be used to apply modules to a subset of the entire rig
class FixtureGroup(object):
	def __init__(self, rig, id, fixtures):
		self.rig = rig
		self.id = id
		self.fixture = []
		self.rect = None #(xMin, yMin, xMax, yMax)
		for fixId in fixtures: #turn fixture id list into list of fixture references
			fixture = rig.fixture[fixId]
			self.fixture.append(fixture)
			if self.rect == None:
				self.rect = fixture.rect
			else:
				self.rect = (min(self.rect[0], fixture.rect[0]), min(self.rect[1], fixture.rect[1]), max(self.rect[2], fixture.rect[2]), max(self.rect[3], fixture.rect[3]))
		self.center = ((self.rect[2] - self.rect[0])/2, (self.rect[3] - self.rect[1])/2)
	
	def interp(self, lightSource, type, speed):
		updates = []
		for fixture in self.fixture:
			updates += fixture.interp(lightSource, type, speed)
		return updates
	def setAll(self, color=None, intensity=None):
		updates = []
		for fixture in self.fixture:
			updates += fixture.setAll(color, intensity)
		return updates
