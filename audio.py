import pyaudio
import threading
import queue


class output (threading.Thread):
	def __init__(self, fs):
		self.q = queue.Queue(1)
		threading.Thread.__init__(self)
		pya = pyaudio.PyAudio()
		self.stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=fs, output=True)


	def run(self):
		while True:
			self.stream.write(self.q.get())

	def write(self, audio):
		self.q.put(audio)

