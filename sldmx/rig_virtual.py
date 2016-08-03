from Tkinter import *

class VirtualRig(object):
	def __init__(self):
		self.gui = Tk()
		self.canvas = Canvas(self.gui, width=500, height=200)
		self.canvas.pack(fill=BOTH, expand=1)
		self.centerX = int(self.canvas["width"])/2
		self.centerY = int(self.canvas["height"])/2		
		def _create_circle(self, x, y, r, **kwargs):
			return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
		Canvas.create_circle = _create_circle
	def start(self, tick, cb):
		self.tick = tick
		self.cb = cb
		self.gui.after(tick, cb)
		self.gui.mainloop()
	def update(self):
		self.gui.after(self.tick, self.cb)  # reschedule event
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