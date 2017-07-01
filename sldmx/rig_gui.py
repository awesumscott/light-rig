try:
	import Tkinter as tk #Python2
except ImportError:
	import tkinter as tk #Python3

class Gui(object):
	def __init__(self, rig):
		
		self.rig = rig
		self.tk = tk
		self.app = tk.Tk()
		self.callbacks = []
		#self.isStarted = False
		
		self.app.after(rig.TICK_INTERVAL, self._tkStep)
	def start(self):
		#self.showGradientDialog()
		self.app.mainloop()
	def stop(self):
		self.app.quit()
	def addCallback(self, cb):
		self.callbacks.append(cb)
	def _tkStep(self):
		self.app.after(self.rig.TICK_INTERVAL, self._tkStep)
		for cb in self.callbacks:
			cb()
	def showGradientDialog(self, dest):
		popup = tk.Toplevel(self.rig.gui.app)
		self.gradientDialog = GradientDialog(popup, self.rig, dest)

from sldmx.rig_colors import *
class GradientDialog(tk.Frame):
	CELL_SIZE = 20
	def __init__(self, parent, rig, dest, *args, **kwargs):
		tk.Frame.__init__(self, parent)
		self.rig = rig
		self.dest = dest
		c = tk.Canvas(self)
		c.pack(padx=0, pady=10)
		c.bind("<Button-1>", self._mouseDown)
		c.bind("<Motion>", self._motion)
		c.bind("<Configure>", self._configure)
		self.c = c
		self.color1 = red
		self.color2 = blue
		self.color3 = black
		self.pack()
	def _mouseDown(self, event):
		print("%s%s" % (event.x, event.y))
	def _motion(self, event):
		#380x266 ?
		
		width=420
		height=280
		
		hratio = 1-float(event.x)/width
		vratio = 1-float(event.y)/height
		
		hcolor = tuple(int(c2+((c1-c2)*hratio)) for c1, c2 in zip(self.color1, self.color2))
		ncolor = tuple(int(c2+((c1-c2)*vratio)) for c1, c2 in zip(hcolor, self.color3))
		
		self.c.configure(background="#%02x%02x%02x" % ncolor)
		#if (len(self.rig.modules)):
		#	self.rig.modules[0].color = ncolor
		#self.dest[0:3] = ncolor[0:3]
		self.dest.color = ncolor
		
	def _configure(self, event=None):
		self.c.delete("gradient")
		width=420
		height=280
		
		hratio = tuple(float(c2-c1)/width for c1,c2 in zip(self.color1, self.color2))
		
		for i in range(int(width/GradientDialog.CELL_SIZE)):
			x = i * GradientDialog.CELL_SIZE
			hcolor = tuple(int(c + (r * x)) for c,r in zip(self.color1, hratio))
			vratio = tuple(float(c2-c1)/height for c1,c2 in zip(hcolor, self.color3))
			
			for j in range(int(height/GradientDialog.CELL_SIZE)):
				y = j * GradientDialog.CELL_SIZE
				ncolor = tuple(int(c + (r * y)) for c,r in zip(hcolor, vratio))
				
				color = "#%02x%02x%02x" % ncolor
				self.c.create_rectangle(x, y, x + GradientDialog.CELL_SIZE, y + GradientDialog.CELL_SIZE, tags=("gradient",), fill=color, width=0)
				#break #uncomment this to test mousemove color detection
			self.c.create_rectangle(x, y + GradientDialog.CELL_SIZE, x + GradientDialog.CELL_SIZE, y + 2 * GradientDialog.CELL_SIZE, tags=("gradient",), fill="#%02x%02x%02x" % self.color3, width=0)
		self.c.lower("gradient")

