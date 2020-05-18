import numpy as np
import simpleaudio as sa
import psutil
import time
import sys
import getpass
from colors import color
import sin
import audio
import os
fs = 44100  # 44100 samples per second

first = True
tau = 0.05

processes = []
sines = []


for pid in psutil.pids():
	p = psutil.Process(pid)
	if p.username() == getpass.getuser() and pid != os.getpid() :#and p.name() == "top":
	#if sys.argv[1] in p.name():
		processes.append(p)

	frequency = 440*np.logspace(-1, 1.58496250072, len(processes), base=2)

for p in range(len(processes)):
	sines.append(sin.Sin(frequency[p], fs, tau))


def print_waterfall(percents):
	for percent in percents:
		strength = int(percent/100*255)
		rgb = (strength, strength, strength)
		print(color(' ', rgb, rgb), end="")

	print()

stream = audio.output(fs)
stream.start()

while True:
	percents = np.array([p.cpu_percent() for p in processes])

	for p in range(len(percents)):
		sines[p].set_amplitude(percents[p])


	width = 50
	seconds = 0.1  # Note duration of 3 seconds

	# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
	t = np.linspace(0, seconds, int(seconds * fs), False)

	# Generate a 440 Hz sine wave
	note = sum([sinus.get_seconds(seconds) for sinus in sines])
	#note = sum([percents[i] * np.sin(frequency[i] * t * 2 * np.pi) for i in range(len(percents))])


	# Ensure that highest value is in 16-bit range
	audio = note * (2**15 - 1)/max(100, np.max(np.abs(note)))
	# Convert to 16-bit data
	audio = audio.astype(np.int16).tobytes()

	stream.write(audio)

	print_waterfall(percents)

