import pyaudio
import threading


class output (threading.Thread):
	def __init__(self, fs):
		threading.Thread.__init__(self)
		pya = pyaudio.PyAudio()
		self.stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=fs, output=True)


	def run(self):
		while True:
			sleep(1)

	def write(self, audio):
		self.stream.write(audio)

