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
fader2 = 0
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
	rig.colorList = []
	rig.colorList.append(colorListPresets[i])
	#rig.modules.clear()
	
	#rig.colorList.append(colorListPresets[i+1])
def setSingleColorLists():
	global fader
	rig.colorList = []
	rig.colorList.append([red])
	rig.colorList.append([blue])
	fader = ModFader(rig, 0, 0)
	rig.modules.add(fader)
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

def startTransition():
	global fader
	if len(rig.modules) < 1: return
	newFader = ModFader(rig, 0, 1)
	rig.modules[0].replaceWith(ModTransition(rig, fader, newFader, .5))
	fader = newFader

def startChase():
	rig.modules.add(ModChase(rig, 0, [LightSource(1, chaseColor, 1.2)], 1, .05))
def setChaseColor(data):
	global chaseColor
	index = int(data) - 1
	chaseColor = colorPresets[max(min(index, len(colorPresets) - 1), 0)]

def strobeDelay():
	rig.modules.add(
		ModDelay(rig, 
			ModSelfDestruct(rig, 
				ModStrobe(rig, 0, 6),
				2
			),
			2
		)
	)

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
	
	return
	
	p1 = ModGroup(rig)
	p1.add(ModFill(rig, curGroup, red, .5))
	#p1.add(ModFill(rig, curGroup, None, .5))
	presets.append(p1)
	
	p2 = ModGroup(rig)
	p2.add(ModFill(rig, curGroup, green, .5))
	presets.append(p2)
	
	p3 = ModGroup(rig)
	p3.add(ModFill(rig, curGroup, blue, .5))
	presets.append(p3)
	presetIndex = 0
	rig.modules.add(presets[presetIndex])
	
def preset1():
	if len(rig.presets):
		rig.loadPreset("a")
	return
	
	global presetIndex
	if len(presets) < 1: return
	if presets[presetIndex] == presets[0]: return
	presetIndex = 0
	rig.modules[0].replaceWith(ModTransition(rig, rig.modules[0], presets[presetIndex], 1.))
	
def preset2():
	if len(rig.presets):
		rig.loadPreset("b")
	return
	
	global presetIndex
	if len(presets) < 2: return
	if presets[presetIndex] == presets[1]: return
	presetIndex = 1
	rig.modules[0].replaceWith(ModTransition(rig, rig.modules[0], presets[presetIndex], 1.))
	
def preset3():
	if len(rig.presets):
		rig.loadPreset("c")
	return
	
	global presetIndex
	if len(presets) < 3: return
	if presets[presetIndex] == presets[2]: return
	presetIndex = 2
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
rig = Rig(1, True)

rig.menu.addAction('1', "Adding fader", addFader)

#acm = colorMenu.addMenu('1', "Add color!")
colorMenu = rig.addMenu('2', "Color menu")
colorMenu.addAction('1', "Adding preset color", addColor, 1)
colorMenu.addAction('2', "Adding preset color list", setColorList, 1)
colorMenu.addAction('3', "Setting single color lists", setSingleColorLists)
colorMenu.addAction('4', "Setting chase color", setChaseColor, 1)
colorMenu.addAction('9', "Clearing color list", clearColors)

rig.menu.addAction('4', "Starting transition module", startTransition)
rig.menu.addAction('6', "Starting delayed strobe", strobeDelay)
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

rig.menu.addAction('a', "Switching to Preset 1", preset1)
rig.menu.addAction('b', "Switching to Preset 2", preset2)
rig.menu.addAction('c', "Switching to Preset 3", preset3)
rig.menu.addAction('g', "Gradient color picker dialog", gradientTester)

#TODO: implement this syntax for anims:
#v = lambda: ModFader(rig, 0, 1)
#Anim(Mod1()).then(v)

rig.start()
