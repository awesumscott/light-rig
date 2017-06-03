import importlib

class Input(object):
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
	def start(self):
		with ConsoleStream(self) as cstream:
			self.cs = cstream
	
	def getKey(self):
		if self._windows:
			if self.msvcrt.kbhit():
				return Input._standardize(self.msvcrt.getch().decode("utf-8"))
		else:
			if self.cs != None:
				d = self.cs.get_data()
				if d != '\x1b' and d != False:
					return Input._standardize(d)
	
	def _standardize(s):
		s = s.lower()
		s = "\n" if s == "\r" else s
		return s

class ConsoleStream(object):
	def __enter__(self, input):
		self.old_settings = input.termios.tcgetattr(input.sys.stdin)
		input.tty.setcbreak(input.sys.stdin.fileno())
		return self

	def __exit__(self, type, value, traceback):
		input.termios.tcsetattr(input.sys.stdin, input.termios.TCSADRAIN, self.old_settings)

	def get_data(self):
		if input.select.select([input.sys.stdin], [], [], 0) == ([input.sys.stdin], [], []):
			return input.sys.stdin.read(1)
		return False