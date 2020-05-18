import numpy as np
import simpleaudio as sa
import psutil
import time
import sys
import getpass

print(sys.argv)

first = True
play_job = None
processes = []
for pid in psutil.pids():
	p = psutil.Process(pid)
	if p.username() == getpass.getuser():
	#if sys.argv[1] in p.name():
		processes.append(p)
play_obj = None

while True:
	time.sleep(0.05)
	percents = np.array([p.cpu_percent() for p in processes])

	width = 50
	frequency = np.linspace(440, 1000, len(percents))#200*percent  # Our played note will be 440 Hz
	fs = 44100  # 44100 samples per second
	seconds = 0.5  # Note duration of 3 seconds

	# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
	t = np.linspace(0, seconds, int(seconds * fs), False)

	# Generate a 440 Hz sine wave
	note = sum([percents[i] * np.sin(frequency[i] * t * 2 * np.pi) for i in range(len(percents))])

	# Ensure that highest value is in 16-bit range
	audio = note * (2**15 - 1) / np.max(np.abs(note))
	#if percent <= 10:
	#	audio *= 0
	#else:
	#	audio *= percent/100
	# Convert to 16-bit data
	audio = audio.astype(np.int16)


	# Start playback
	if not first:
		play_obj.stop()
	play_obj = sa.play_buffer(audio, 1, 2, fs)
	first = False
	# Wait for playback to finish before exiting
