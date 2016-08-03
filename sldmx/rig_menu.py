class RigMenu(object):
	def __init__(self, key, title):
		self.title = title	#message to print when entering this menu
		self.key = key		#character that opens this menu from its parent
		self.children = []
	def addMenu(self, key, title):
		m = RigMenu(key, title)
		self.children.append(m)
		return m
	def addAction(self, key, title, func, numChars = 0):
		a = RigMenuAction(key, title, func, numChars)
		self.children.append(a)
		return a
	def run(self):
		print self.title

class RigMenuAction(object):
	def __init__(self, key, title, func, numChars = 0):
		self.key = key
		self.title = title
		self.callback = func
		self.collectChars = numChars
		self.data = ""