
class VirtualRig(object):
	def __init__(self, rig):
		self.rig = rig
		rig.initGui()
		self.canvas = rig.gui.tk.Canvas(rig.gui.app, width=1000, height=500)
		self.canvas.pack(fill=rig.gui.tk.BOTH, expand=1)
		self.centerX = int(self.canvas["width"]) / 2
		self.centerY = int(self.canvas["height"]) / 2		
		def _create_circle(self, x, y, r, **kwargs):
			return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
		rig.gui.tk.Canvas.create_circle = _create_circle
	def start(self):
		self.rig.gui.addCallback(self._step)
		self.rig.gui.start()
	def _step(self):
		self.rig.step()
		for fixture in self.rig.fixture:
			f = self.rig.fixture[fixture]
			for light in f.light:
				self.setLight(light.virtualLight, '#%02x%02x%02x'%light.output())
	def addLight(self, newLight, lightX, lightY, numLights):
		if numLights > 1:	#rectangle
			rhalf = 20
			spacing = 40
			newLight.virtualLight = self.canvas.create_rectangle(
				self.centerX + lightX * spacing - rhalf,
				self.centerY - lightY * spacing - rhalf,
				self.centerX + lightX * spacing + rhalf,
				self.centerY - lightY * spacing + rhalf,
				outline="#f00", fill="#fb0")
		else:				#circle
			newLight.virtualLight = self.canvas.create_circle(
				self.centerX + lightX * 30,
				self.centerY + lightY * 20,
				20,
				outline="#000", fill="#fb0")
	def setLight(self, light, color):
		self.canvas.itemconfig(light, fill=color)
