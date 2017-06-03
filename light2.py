from sldmx import *

red = (255, 0, 0)
orange = (255, 45, 0)
yellow = (255, 127, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
white = (255, 255, 255)
blue = (0, 0, 255)
purple = (255, 0, 255)
pink = (255, 0, 127)
halfWhite = (127, 127, 127)
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
blank = False

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
	#rig.colorList.append(colorListPresets[i+1])
def setSingleColorLists(data):
	global fader
	rig.colorList = []
	rig.colorList.append([(255, 0, 0)])
	rig.colorList.append([(0, 0, 255)])
	fader = ModFader(rig, 0, 0)
	rig.modules.add(fader)
def clearColors(data):
	rig.colorList = []
def setCurGroup(data):
	global curGroup
	curGroup = int(data)
	global fader
	fader.group = curGroup

def impulse(data):
	global curGroup
	rig.modules.add(ModImpulse(rig, curGroup))

def addFader(data):
	global fader
	fader = rig.modules.add(ModFader(rig, 0, 0))

def startTransition(data):
	global fader
	if len(rig.modules) < 1: return
	newFader = ModFader(rig, 0, 1)
	rig.modules[0].replaceWith(ModTransition(rig, fader, newFader, .5))
	fader = newFader

def startChase(data):
	rig.modules.add(ModChase(rig, 0, [LightSource(1, (255,255,255), 1.2)], 1, .05))

def strobeDelay(data):
	rig.modules.add(
		ModDelay(rig, 
			ModSelfDestruct(rig, 
				ModStrobe(rig, 0, 6),
				2
			),
			2
		)
	)

def pop(data):
	rig.modules.pop()
def toggleBlank(data):
	global blank
	if blank:
		rig.modules.pop()
	else:
		rig.modules.add(ModFill(rig, curGroup, None, 0.))
	blank = not blank

rig = Rig(2, True)
rig.menu.addAction('1', "Adding fader", addFader)

#acm = colorMenu.addMenu('1', "Add color!")
colorMenu = rig.addMenu('2', "Color menu")
colorMenu.addAction('1', "Adding preset color", addColor, 1)
colorMenu.addAction('2', "Adding preset color list", setColorList, 1)
colorMenu.addAction('3', "Setting single color lists", setSingleColorLists)
colorMenu.addAction('9', "Clearing color list", clearColors)

rig.menu.addAction('4', "Starting transition module", startTransition)
rig.menu.addAction('5', "Adding chase", startChase)
rig.menu.addAction('6', "Starting delayed strobe", strobeDelay)
rig.menu.addAction('p', "Popping last module added", pop)
rig.menu.addAction('9', "Setting current group", setCurGroup, 1)
rig.menu.addAction(' ', "Toggle Blankness", toggleBlank)
rig.menu.addAction('\n', "Impulse", impulse)

#TODO: implement this syntax for anims:
#v = lambda: ModFader(rig, 0, 1)
#Anim(Mod1()).then(v)

rig.start()