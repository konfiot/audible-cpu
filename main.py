import numpy as np
import simpleaudio as sa
import psutil
import time
import sys
import getpass
from colors import color
import sin
import audio

fs = 44100  # 44100 samples per second

first = True
tau = 0.05

processes = []
sines = []


for pid in psutil.pids():
	p = psutil.Process(pid)
	if p.username() == getpass.getuser() and p.name() == "top":
	#if sys.argv[1] in p.name():
		processes.append(p)

	frequency = np.linspace(440, 3000, len(processes))

for p in range(len(processes)):
	sines.append(sin.Sin(frequency[p], fs, tau))


def print_waterfall(percents):
	for percent in percents:
		strength = int(percent/100*255)
		rgb = (strength, strength, strength)
		print(color(' ', rgb, rgb), end="")

	print()

stream = audio.output(fs)

while True:
	percents = np.array([p.cpu_percent() for p in processes])

	print(percents)

	for p in range(len(percents)):
		sines[p].set_amplitude(percents[p])


	width = 50
	seconds = 0.1  # Note duration of 3 seconds

	# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
	t = np.linspace(0, seconds, int(seconds * fs), False)

	# Generate a 440 Hz sine wave
	print("test")
	print(len(sines))
	note = sum([sinus.get_seconds(seconds) for sinus in sines])
	#note = sum([percents[i] * np.sin(frequency[i] * t * 2 * np.pi) for i in range(len(percents))])


	print("test")
	# Ensure that highest value is in 16-bit range
	audio = note * (2**15 - 1)/100
	# Convert to 16-bit data
	print(audio)
	audio = audio.astype(np.int16).tobytes()

	stream.write(audio)

	print_waterfall(percents)

