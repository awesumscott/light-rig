import json, array
from rig_menu import *
from rig_utils import Timer, easeCircle
from rig_input import Input
from rig_virtual import VirtualRig
from rig_hardware import FixtureGroup, Fixture, Light

TICK_INTERVAL = 20

from mod_group import ModGroup

class Rig(object):
	def __init__(self, config, virtual=False):
		self.menu = RigMenu('.', "Main menu")
		self.activeMenu = self.menu
		self.colorList = [[]]
		self.fixture = {}
		self.group = {}
		self.modules = ModGroup(self)
		#self.virtualFixtures = []
		self.virtual = virtual
		self.canvas = None
		self.input = Input()
		
		if self.virtual:
			self.virtual = VirtualRig()
		else:
			from ola.ClientWrapper import ClientWrapper
		
		jsonData = open('./config/' + str(config) + '.json', 'r')
		data = json.load(jsonData)
		jsonData.close()
		jsonData = open('./config/defs.json', 'r')
		fixDefData = json.load(jsonData)
		jsonData.close()
		
		#load defs
		fixtureDefs = {}
		for fixDef in fixDefData["fixDef"]:
			fixtureDefs[fixDef["id"]] = fixDef
		print fixtureDefs
		
		for fixture in data["fixture"]:
			type = int(fixture["type"])
			fixtureDef = fixtureDefs[type]
			lightData = fixtureDef["light"]
			fixX = fixture["posx"]
			fixY = fixture["posy"]
			numLights = len(lightData)
			channelsSetTo255 = []
			if "channelsSetTo255" in fixtureDef:
				channelsSetTo255 = fixtureDef["channelsSetTo255"]
			newFixture = Fixture(fixture["id"], fixtureDef["channels"], fixture["universe"], fixX, fixY, channelsSetTo255)
			self.fixture[fixture["id"]] = newFixture
			for light in lightData:
				lightX = light["posx"] + fixX
				lightY = light["posy"] + fixY
				newLight = Light(light["rgb"], lightX, lightY)
				if self.virtual:
					self.virtual.addLight(newLight, lightX, lightY, numLights)
					
				newFixture.addLight(newLight)
		print self.fixture
		if "group" in data:
			for group in data["group"]:
				groupId = group["id"]
				self.group[groupId] = FixtureGroup(self, groupId, group["fixtures"])
					
		#	if "defaultgroup" in data:
		#		self.group_index = data["defaultgroup"]
			
	def virtualGuiUpdate(self):
		self.step()
		
		for fixture in self.fixture:
			f = self.fixture[fixture]
			for light in f.light:
				self.virtual.setLight(light.virtualLight, '#%02x%02x%02x'%light.output())
		
		self.virtual.update()
	def lightUpdate(self):
		#TODO: make a universes dict, if fix univ isn't in dict, make new 512 array, add output to dict byte arrays, SendDmx each univ array
		global TICK_INTERVAL
		self.wrapper.AddEvent(TICK_INTERVAL, self.lightUpdate)
		self.step()
		data = array.array('B')
		for fixture in self.fixture:
			f = self.fixture[fixture]
			bytes = f.output()
			for b in bytes:
				data.append(b)
		
		self.wrapper.Client().SendDmx(0, data, self.DmxSent)
		
	def DmxSent(self, state):
		if not state.Succeeded():
			print state.message
			self.wrapper.Stop()
		
	def start(self):
		global TICK_INTERVAL
		if self.virtual:
			self.virtual.start(TICK_INTERVAL, self.virtualGuiUpdate)
		
		self.input.start()
		
		if not self.virtual:
			self.wrapper = ClientWrapper()
			self.wrapper.AddEvent(TICK_INTERVAL, self.lightUpdate)
			self.wrapper.Run()
	
	def step(self):
		key = self.input.getKey()
		if key != None:
			if key == "\r":
				key = "\n"
			key = key.lower()
			
			if type(self.activeMenu) is RigMenuAction:
				m = self.activeMenu
				if m.collectChars > 0 and len(m.data) < m.collectChars:
					m.data += key
				if len(m.data) == m.collectChars:
					m.callback(m.data)
					m.data = ""
					self.activeMenu = self.menu
			else:
				for m in self.activeMenu.children:
					if m.key == key:
						if type(m) is RigMenu:
							self.activeMenu = m
							m.run()
						elif type(m) is RigMenuAction:
							if m.collectChars == 0:
								print m.title
								m.callback(m.data)
								m.data = ""
								self.activeMenu = self.menu
							else:
								print "Enter " + str(m.collectChars) + " characters"
								self.activeMenu = m
							
						break
		
		updates = self.modules.run()
		
		for u in updates:
			light = self.fixture[u.fixId].light[u.lightId]
			if u.color != None:
				if u.easing == None:
					light.color = u.color
				else:
					light.color = u.easing(light.color, u.color, *u.params)
			if u.intensity != None:
				light.intensity = u.intensity
	
	def addMenu(self, key, title):
		return self.menu.addMenu(key, title);
