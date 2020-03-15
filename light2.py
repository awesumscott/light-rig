from sldmx import *
import json

colorPresets = (red, orange, yellow, green, cyan, white, blue, purple, pink)
colorListPresets = [
	[red, purple, blue, purple], #"3D" or "Po-lice"
	[red, yellow, green, yellow], #"Reggae"
	[red, orange, yellow, orange], #"Fire"
	[green, cyan, blue, cyan, green], #"Seawater"
	[red, purple, pink, purple], #"Valentine"
	[red, halfWhite, green, halfWhite, blue, halfWhite], #"RGB"
	[green, (45, 255, 0), (45, 255, 15)] #"St Pattys"
]
fader = 0
curGroup = 0
blank = None
strobeModule = None
chaseColor = white

presets = [] #list of module presets loaded for songs
presetIndex = 0

def addColor(data):
	c = colorPresets[int(data)-1]
	print("Added " + str(c))
	rig.colorList[0].append(c)
def setColorList(data):
	i = int(data)-1
	if i >= len(colorListPresets):
		print("Color list index out of bounds, using list 1 instead")
		i = 0
	else:
		print("New color list set!")
	rig.colorList = [colorListPresets[i]]
	#rig.modules.clear()

def clearColors():
	rig.colorList = []
def setCurGroup(data):
	global curGroup
	curGroup = int(data)
	global fader
	fader.group = curGroup

def impulse():
	global curGroup
	rig.modules.add(ModImpulse(rig, curGroup, 2))

def addFader():
	global fader
	rig.modules.clear()
	rig.modules.add(ModFill(rig, 0, None, Light.IntensityBase))
	fader = rig.modules.add(ModFader(rig, 0, 0))

def startChase():
	rig.modules.add(ModChase(rig, 0, [LightSource(1, chaseColor, 1.2)], 1, .05))
def setChaseColor(data):
	global chaseColor
	index = int(data) - 1
	chaseColor = colorPresets[max(min(index, len(colorPresets) - 1), 0)]

def toggleBlank():
	global blank
	if blank:
		rig.modules.remove(blank)
		blank = None
	else:
		blank = ModFill(rig, curGroup, None, 0.)
		rig.modules.add(blank)

def toggleStrobe():
	global strobeModule
	if strobeModule:
		rig.modules.remove(strobeModule)
		strobeModule = None
	else:
		strobeModule = ModStrobe(rig, curGroup, 3)
		rig.modules.add(strobeModule)

def addStatic():
	rig.modules.add(ModStatic(rig, curGroup, 1))

def setSongPresets(data):
	global presets
	global presetIndex
	
	loader = Loader(rig)
	if (not loader.load(str(data))): return
	
def preset(key):
	if len(rig.presets):
		rig.loadPreset(key)

def preset1():
	global presetIndex
	if len(presets) < 1: return
	if presets[presetIndex] == presets[0]: return
	presetIndex = 0
	rig.modules[0].replaceWith(ModTransition(rig, rig.modules[0], presets[presetIndex], 1.))

def gradientTester():
	#create a gradient popup to operate on a
	#fill module for a group containing all the lights
	rig.initGui()
	fill = ModFill(rig, 0, black, 1.)
	rig.modules.add(fill)
	rig.gui.showGradientDialog(fill)

def printStatus():
	print(rig.modules)

def cls():
	print("\033c")

cls()
rig = Rig(1, False)

rig.menu.addAction('1', "Adding fader", addFader)

#acm = colorMenu.addMenu('1', "Add color!")
colorMenu = rig.addMenu('2', "Color menu")
colorMenu.addAction('1', "Adding preset color", addColor, 1)
colorMenu.addAction('2', "Adding preset color list", setColorList, 1)
colorMenu.addAction('4', "Setting chase color", setChaseColor, 1)
colorMenu.addAction('9', "Clearing color list", clearColors)

rig.menu.addAction('p', "Popping last module added", rig.modules.pop)
rig.menu.addAction('9', "Setting current group", setCurGroup, 1)
rig.menu.addAction(' ', "Toggle Blankness", toggleBlank)
rig.menu.addAction('\n', "Impulse", impulse)
rig.menu.addAction('/', "Enter 3-digit song ID", setSongPresets, 3)
rig.menu.addAction('.', "Tap", rig.tempo.tap)
rig.menu.addAction('s', "Status", printStatus)
#rig.menu.addAction('a', "Impulse", impulse)
rig.menu.addAction('z', "Adding chase", startChase)
rig.menu.addAction('x', "Toggle strobe", toggleStrobe)
rig.menu.addAction('v', "Adding static", addStatic)
rig.menu.addAction('g', "Gradient color picker dialog", gradientTester)

rig.menu.addAction('a', "Switching to Preset a", lambda : preset('a'))
rig.menu.addAction('b', "Switching to Preset b", lambda : preset('b'))
rig.menu.addAction('c', "Switching to Preset c", lambda : preset('c'))
rig.menu.addAction('d', "Switching to Preset d", lambda : preset('d'))

#TODO: implement this syntax for anims:
#v = lambda: ModFader(rig, 0, 1)
#Anim(Mod1()).then(v)

rig.start()
