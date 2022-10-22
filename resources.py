
import pandas as pd
import numpy as np
import math


def add_noise(snr_dB, signal):
    power= signal ** 2
    siganl_average_power = np.mean(power)
    
    signalpower_db = 10*np.log10(power)
    siganl_average_power_dB= 10*np.log10(siganl_average_power)
    noise_dB = siganl_average_power_dB - snr_dB
    noise_watts= 10**(noise_dB/ 10)
    mean_noise=0
    noise=np.random.normal(mean_noise, np.sqrt(noise_watts), len(signal))
    noise_signal= signal+ noise
    return noise_signal

def reconstruct(time):
      sum=0
      for i in range(-sample_freq, sample_freq, 1):
          #signal=amplitude * np.sin(2 * np.pi *freq* i*T)
          sum += genratedsignal*np.sinc((time- i*T)/T) 
      return sum

def get_max_freq(magnitude=[],time=[]):
    sample_period = time[1]-time[0]
    n_samples = len(time)
    fft_magnitudes=np.abs(np.fft.fft(magnitude))
    fft_frequencies = np.fft.fftfreq(n_samples, sample_period)
    fft_clean_frequencies_array = []
    for i in range(len(fft_frequencies)):
        if fft_magnitudes[i] > 0.001:
            fft_clean_frequencies_array.append(fft_frequencies[i])
    max_freq = max(fft_clean_frequencies_array)
    return max_freq


def round_to_nearest(n, m):
    return m * math.ceil(n / m)

def take_samples(time, signal_magnitude, rate):
    step = time[1]-time[0]
    max_freq = get_max_freq(signal_magnitude, time)
    T = 1/max_freq
    df = pd.DataFrame({"time":time, "Amplitude":signal_magnitude})

    sample_rate = rate * max_freq
    T_sample = 1/sample_rate
    sample_t = np.arange(T/4, df['time'].iloc[-1], T_sample)

    sample_amplitude = []

    for v in sample_t:
        sample_amplitude.append(df.iloc[int(round(round_to_nearest(v, step),10)/step)]['Amplitude'])
        
    return (sample_t  ,  sample_amplitude)

def sinc_interpolation(input_magnitude, input_time, original_time):
    '''Whittaker Shannon interpolation formula linked here:
      https://en.wikipedia.org/wiki/Whittaker%E2%80%93Shannon_interpolation_formula '''

    if len(input_magnitude) != len(input_time):
        print('not same')

    # Find the period
    if len(input_time) != 0:
        T = input_time[1] - input_time[0]

    # the equation
    sincM = np.tile(original_time, (len(input_time), 1)) - \
        np.tile(input_time[:, np.newaxis], (1, len(original_time)))
    output_magnitude = np.dot(input_magnitude, np.sinc(sincM/T))
    return output_magnitude

class tap:
    def __init__(self, magnitude=None, time=None, label=None, source = "generate" , amplitude = 5,frequency=20 ,sample_rate=2, noise_checkbox = False, snr=1000):
        self.label = label
        self.source = source
        self.magnitude = magnitude
        self.time = time
        self.sample_rate = sample_rate
        self.noise_checkbox = noise_checkbox
        self.snr = snr
        self.amplitude = amplitude
        self.frequency = frequency

    def set_attributes(self, magnitude=None, time=None, label=None, source = "generate" , amplitude = 5,frequency=20 ,sample_rate=2, noise_checkbox = False, snr=1000):
        self.label = label
        self.source = source
        self.magnitude = magnitude
        self.time = time
        self.sample_rate = sample_rate
        self.noise_checkbox = noise_checkbox
        self.snr = snr
        self.amplitude = amplitude
        self.frequency = frequency

def convert_df(df):
    return df.to_csv().encode('utf-8')