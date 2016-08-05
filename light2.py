from sldmx import *

#               red          orange        yellow          green       cyan           white            blue         purple         pink
colorPresets = ((255, 0, 0), (255, 45, 0), (255, 127, 0), (0, 255, 0), (0, 255, 255), (255, 255, 255), (0, 0, 255), (255, 0, 255), (255, 0, 127))
colorListPresets = [
	[(255, 0, 0), (255, 0, 255), (0, 0, 255), (255, 0, 255)], #"3D" or "Po-lice"
	[(255, 0, 0), (255, 127, 0), (0, 255, 0), (255, 127, 0)], #"Reggae"
	[(255, 0, 0), (255, 45, 0), (255, 127, 0), (255, 45, 0)], #"Fire"
	[(0, 255, 0), (0, 255, 255), (0, 0, 255), (0, 255, 255), (0, 255, 0)], #"Seawater"
	[(255, 0, 0), (255, 0, 255), (255, 0, 127), (255, 0, 255)], #"Valentine"
	[(255, 0, 0), (127, 127, 127), (0, 255, 0), (127, 127, 127), (0, 0, 255), (127, 127, 127)], #"RGB"
	[(0, 255, 0), (45, 255, 0), (45, 255, 15)] #"St Pattys"
]
fader = 0
fader2 = 0
curGroup = 0

def addColor(data):
	c = colorPresets[int(data)-1]
	print "Added " + str(c)
	rig.colorList[0].append(c)
def setColorList(data):
	i = int(data)-1
	if i >= len(colorListPresets):
		print "Color list index out of bounds, using list 1 instead"
		i = 0
	else:
		print "New color list set!"
	rig.colorList = []
	rig.colorList.append(colorListPresets[i])
	rig.colorList.append(colorListPresets[i+1])
def setSingleColorLists(data):
	rig.colorList = []
	rig.colorList.append([(255, 0, 0)])
	rig.colorList.append([(0, 0, 255)])
	fader = ModFader(rig, 0, 0)
def clearColors(data):
	rig.colorList = [[]]
def setCurGroup(data):
	global curGroup
	curGroup = int(data)
	global fader
	fader.group = curGroup

def impulse(data):
	global curGroup
	#rig.modules.add(ModImpulse(rig, curGroup))
	rig.modules.add(ModImpulse, curGroup)

def addFader(data):
	global fader
	global fader2
	#fader = ModFader(rig, 1, 0)
	#rig.modules.add(fader)
	#rig.colorList.append([])
	#fader2 = ModFader(rig, 2, 1)
	#rig.modules.add(fader2)
	fader = rig.modules.add(ModFader, 0, 0)

def startTransition(data):
	global fader
	newFader = ModFader(rig, 0, 1)
	fader.replaceWith(ModTransition(rig, fader, newFader, .5))
	fader = newFader

def startChase(data):
	rig.modules.add(ModChase, 0, [LightSource(1, (255,255,255), 1.5)], 1, .05)

def strobeDelay(data):
	rig.modules.add(ModDelay, ModSelfDestruct(rig, ModStrobe(rig, 0, 6), 5), 5)

rig = Rig(1, True)
colorMenu = rig.addMenu('2', "Color menu")
rig.menu.addAction('1', "Adding fader", addFader)
#acm = colorMenu.addMenu('1', "Add color!")
colorMenu.addAction('1', "Adding preset color", addColor, 1)
colorMenu.addAction('2', "Adding preset color list", setColorList, 1)
colorMenu.addAction('3', "Setting single color lists", setSingleColorLists)
colorMenu.addAction('9', "Clearing color list", clearColors)
rig.menu.addAction('4', "Starting transition module", startTransition)
rig.menu.addAction('5', "Adding chase", startChase)
rig.menu.addAction('6', "Starting delayed strobe", strobeDelay)
rig.menu.addAction('9', "Setting current group", setCurGroup, 1)
rig.menu.addAction('\n', "Impulse", impulse)

#TODO: implement this syntax for anims:
#v = lambda: ModFader(rig, 0, 1)
#Anim(Mod1()).then(v)

rig.start()