import json
from sldmx.mod_beat import ModBeat
from sldmx.mod_delay import ModDelay
from sldmx.mod_fill import ModFill
from sldmx.mod_impulse import ModImpulse
from sldmx.mod_static import ModStatic

class Loader(object):
	TICK_INTERVAL = 20
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
		
		self.rig.colorList = data["colorLists"]
		
		self.rig.presets = {}
		if "presets" in data:
			for preset in data["presets"]:
				self.rig.presets[preset["key"]] = preset["modules"]
		#if "modules" in data:
		#	mods = data["modules"]
		#	for mod in mods:
		#		modType = mod["type"]
		#		if modType == "fill":
					
		#"presets": [
		#{	"key": "a",
		#	"modules": [
		#		{	"type": "fill",
		#			"params": {
		#				"color": [255, 0, 0],
		#				"intensity": 0.5,
		#				"group": 0
		
		print('Song loaded: "' + data['name'] + '" by ' + data['artist'])
		
		return True
	
	@staticmethod
	def loadPreset(rig, key):
		if key in rig.presets:
			rig.modules.clear()
			preset = rig.presets[key]
			for mod in preset:
				rig.modules.add(Loader._loadModule(rig, mod))
	@staticmethod
	def _loadModule(rig, mod):
		modType = mod["type"]
		inflatedParams = Loader._inflateParams(rig, mod["params"])
		if modType == "beat":
			return ModBeat(rig, **inflatedParams)
		elif modType == "delay":
			return ModDelay(rig, **inflatedParams)
		elif modType == "fill":
			return ModFill(rig, **inflatedParams)
		elif modType == "impulse":
			return ModImpulse(rig, **inflatedParams)
		elif modType == "static":
			return ModStatic(rig, **inflatedParams)
	
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
			print(paramType)
			
			if paramType is dict:
				newParams[param] = Loader._loadModule(rig, params[param])
			elif paramType is list:
				newParams[param] = Loader._loadList(rig, params[param])
			else:
				newParams[param] = params[param]
		return newParams

