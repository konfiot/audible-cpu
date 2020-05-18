import numpy as np

class Sin:
	def __init__ (self, frequency, sampling, tau):
		self.frequency = frequency
		self.sampling = sampling
		self.current_amp = 0
		self.target_amp = 0
		self.time = 0
		self.tau = tau

	def set_amplitude(self, amplitude):
		self.target_amp = amplitude

	def get_seconds(self, seconds):
		return self.get_samples(int(seconds*self.sampling))

	def get_samples(self, n_samples):
		out = []

		for i in range(n_samples):
			self.time += 1/self.sampling
			self.current_amp = self.current_amp - (self.current_amp - self.target_amp)/(self.tau*self.sampling)

			sample = self.current_amp*np.sin(self.time*2*np.pi*self.frequency)
			out.append(sample)

		return np.array(out)

