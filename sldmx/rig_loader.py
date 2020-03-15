import json
from sldmx.mod_beat import ModBeat
from sldmx.mod_chase import ModChase
from sldmx.mod_delay import ModDelay
from sldmx.mod_fader import ModFader
from sldmx.mod_fill import ModFill
from sldmx.mod_group import ModGroup
from sldmx.mod_impulse import ModImpulse
from sldmx.mod_selfdestruct import ModSelfDestruct
from sldmx.mod_static import ModStatic
from sldmx.mod_strobe import ModStrobe
from sldmx.rig_colors import Colors

class Loader(object):
	def __init__(self, rig):
		self.rig = rig
	
	def load(self, filename):
		try:
			jsonData = open('./songs/' + filename + '.json', 'r')
			data = json.load(jsonData)
			jsonData.close()
		except FileNotFoundError:
			print("No song config with ID " + str(data))
			return False
		
		if "bpm" in data:
			bpm = int(data["bpm"])
			self.rig.tempo.avg = 60000 / bpm #bpm to ms
		
		#self.rig.colorList = data["colorLists"]
		#all this trouble to stick with tuples, maybe they should change to lists
		if "colorLists" in data:
			self.rig.colorList = []
			for cl in data["colorLists"]:
				nl = []
				for li in cl:
					liType = type(li)
					if liType is list:
						nl.append(tuple(li))
					elif liType is str:
						if li in Colors:
							nl.append(Colors[li])
						#else print error msg
				self.rig.colorList.append(nl)
		
		self.rig.presets = {}
		if "presets" in data:
			for preset in data["presets"]:
				self.rig.presets[preset["key"]] = preset["modules"]
		#if "modules" in data:
		#	mods = data["modules"]
		#	for mod in mods:
		#		modType = mod["type"]
		#		if modType == "fill":
		
		print("GRADIENT SOURCE = " + data["ui"][0]["source"])
		
		print('Song loaded: "' + data['name'] + '" by ' + data['artist'])
		
		return True
	
	@staticmethod
	def loadPreset(rig, key):
		rig.presetRefs = {}
		if key in rig.presets:
			rig.modules.clear()
			preset = rig.presets[key]
			for mod in preset:
				rig.modules.add(Loader._loadModule(rig, mod))
	@staticmethod
	def _loadModule(rig, mod):
		modType = mod["type"]
		inflatedParams = {}
		if "params" in mod:
			inflatedParams = Loader._inflateParams(rig, mod["params"])
		
		if modType == "beat":
			newMod = ModBeat(rig, **inflatedParams)
		elif modType == "chase":
			newMod = ModChase(rig, **inflatedParams)
		elif modType == "delay":
			newMod = ModDelay(rig, **inflatedParams)
		elif modType == "fader":
			newMod = ModFader(rig, **inflatedParams)
		elif modType == "fill":
			newMod = ModFill(rig, **inflatedParams)
		elif modType == "group":
			newMod = ModGroup(rig, **inflatedParams)
		elif modType == "impulse":
			newMod = ModImpulse(rig, **inflatedParams)
		elif modType == "selfdestruct":
			newMod = ModSelfDestruct(rig, **inflatedParams)
		elif modType == "static":
			newMod = ModStatic(rig, **inflatedParams)
		elif modType == "strobe":
			newMod = ModStrobe(rig, **inflatedParams)
		
		if "name" in mod:
			rig.presetRefs[mod["name"]] = newMod
		
		return newMod
	
	@staticmethod
	def _loadList(rig, lst):
		newLst = []
		for li in lst:
			newLst.append(Loader._loadModule(rig, li) if (type(li) is dict) else li)
		return newLst
	
	@staticmethod
	#recursive method to instantiate new module instances from
	#the params of preset definitions from the inside out
	def _inflateParams(rig, params):
		newParams = {}
		for param in params:
			paramType = type(params[param])
			#print(paramType)
			
			if paramType is dict:
				newParams[param] = Loader._loadModule(rig, params[param])
			elif paramType is list:
				newParams[param] = Loader._loadList(rig, params[param])
			else:
				newParams[param] = params[param]
		return newParams

