import importlib

class Input(object):
	ESC = '\x1b'
	def __init__(self):
		try:
			self._windows = False
			
			self.sys = importlib.import_module('sys')
			self.select = importlib.import_module('select')
			self.tty = importlib.import_module('tty')
			self.termios = importlib.import_module('termios')
		except ImportError:
			self._windows = True
			self.msvcrt = importlib.import_module('msvcrt')
		self.cs = None
	
	def getKey(self):
		if self._windows:
			if self.msvcrt.kbhit():
				return Input._standardize(self.msvcrt.getch().decode("utf-8"))
		else:
			if (self.cs == None):
				return False
			d = self.cs.get_data()
			if d != False: #d != Input.ESC and 
				return Input._standardize(d)
	
	#Begins capturing input for an ongoing function, ends when the function ends
	def start(self, callback):
		if self._windows:
			callback()
		else:
			with ConsoleStream(self) as cstream:
				self.cs = cstream
				callback()
	
	@staticmethod
	def _standardize(s):
		s = s.lower()
		s = "\n" if s == "\r" else s
		return s

class ConsoleStream(object):
	def __init__(self, input):
		self._input = input
	def __enter__(self):
		self.old_settings = self._input.termios.tcgetattr(self._input.sys.stdin)
		self._input.tty.setcbreak(self._input.sys.stdin.fileno())
		return self

	def __exit__(self, type, value, traceback):
		self._input.termios.tcsetattr(self._input.sys.stdin, self._input.termios.TCSADRAIN, self.old_settings)

	def get_data(self):
		if self._input.select.select([self._input.sys.stdin], [], [], 0) == ([self._input.sys.stdin], [], []):
			return self._input.sys.stdin.read(1)
		return False
