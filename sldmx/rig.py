import json, array
from sldmx.rig_menu import *
from sldmx.rig_utils import Timer, easeCircle
from sldmx.rig_input import Input
from sldmx.rig_virtual import VirtualRig
from sldmx.rig_hardware import FixtureGroup, Fixture, Light
from ola.ClientWrapper import ClientWrapper
from sldmx.rig_tempo import TapTempo

from sldmx.mod_group import ModGroup
from sldmx.mod_fill import ModFill

class Rig(object):
	TICK_INTERVAL = 20
	def __init__(self, config, virtual=False):
		self.menu = RigMenu('.', "Main menu")
		self.activeMenu = self.menu
		self.exiting = False
		self.colorList = [[]]
		self.fixture = {}
		self.group = {}
		self.modules = ModGroup(self)
		self.virtual = virtual
		self.canvas = None
		self.input = Input()
		self.universes = []
		self.dmxData = {}
		self.tempo = TapTempo()
		self.gui = None

		#self.modules.add(ModFill(self, 0, None, Light.IntensityBase))
		
		if self.virtual:
			self.virtual = VirtualRig(self)
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
		###print(fixtureDefs)
		
		currentChannelOffsets = {}
		for fixture in data["fixture"]:
			type = int(fixture["type"])
			fixtureDef = fixtureDefs[type]
			lightData = fixtureDef["light"]
			
			universe = int(fixture["universe"])
			if (not universe in self.universes):
				self.universes.append(universe)
				self.dmxData[universe] = bytearray([0]*512)
				currentChannelOffsets[universe] = 0
			
			fixX = fixture["posx"]
			fixY = fixture["posy"]
			numLights = len(lightData)
			fixedchannels = []
			if "fixedchannels" in fixtureDef:
				fixedchannels = fixtureDef["fixedchannels"]
			channels = fixtureDef["channels"]
			newFixture = Fixture(fixture["id"], channels, universe, fixX, fixY, fixedchannels)
			newFixture.channelOffset = currentChannelOffsets[universe]
			currentChannelOffsets[universe] += channels
			
			self.fixture[fixture["id"]] = newFixture
			for light in lightData:
				lightX = light["posx"] + fixX
				lightY = light["posy"] + fixY
				newLight = Light(light["rgb"], lightX, lightY)
				if self.virtual:
					self.virtual.addLight(newLight, lightX, lightY, numLights)
					
				newFixture.addLight(newLight)
		#print(self.fixture)
		if "group" in data:
			for group in data["group"]:
				groupId = group["id"]
				self.group[groupId] = FixtureGroup(self, groupId, group["fixtures"])
					
		#	if "defaultgroup" in data:
		#		self.group_index = data["defaultgroup"]
	
	def lightUpdate(self):
		self.wrapper.AddEvent(Rig.TICK_INTERVAL, self.lightUpdate)
		self.step()
		
		for fixture in self.fixture:
			f = self.fixture[fixture]
			bytes = f.output()
			self.dmxData[f.universe][f.channelOffset:f.channelOffset+f.channels] = bytes
		
		for u in self.universes:
			#print("universe " + str(u) + " length = " + str(len(self.dmxData[u])))
			self.wrapper.Client().SendDmx(u, array.array('B', self.dmxData[u]), self.DmxSent)
	def clearLights(self):
		clearData = array.array('B', [0]*512)
		for u in self.universes:
			self.wrapper.Client().SendDmx(u, clearData, self.DmxSent)
		
	def DmxSent(self, state):
		if not state.Succeeded():
			print(state.message)
			self.wrapper.Stop()
		
	def start(self):
		print("Light show started!")
		
		if self.virtual:
			self.input.start(self.virtual.start)
		else:
			self.wrapper = ClientWrapper()
			self.wrapper.AddEvent(Rig.TICK_INTERVAL, self.lightUpdate)
			self.input.start(self.wrapper.Run)
			self.clearLights()
		
		print("Light show ended")
	
	def step(self):
		self.tempo.step()
		key = self.input.getKey()
		if key != None:
			#Exit if Esc is pressed twice
			if (key == Input.ESC):
				if (self.exiting):
					if self.virtual:
						self.gui.stop()
					else:
						self.wrapper.Stop()
					return
				else:
					self.exiting = True
					print("Press ESC again to confirm exit")
			else:
				self.exiting = False
			
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
								print(m.title)
								#m.callback(m.data)
								m.callback()
								m.data = ""
								self.activeMenu = self.menu
							else:
								print("Enter " + str(m.collectChars) + " characters")
								self.activeMenu = m
						break
		
		if self.modules: #len(self.modules):
			updates = self.modules.run()
		else:
			updates = self.group[0].setAll((0,0,0), 0.)
		
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
		return self.menu.addMenu(key, title)
	
	def initGui(self):
		if self.gui: return
		
		from sldmx.rig_gui import Gui
		self.gui = Gui(self)
		
