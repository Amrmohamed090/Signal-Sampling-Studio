
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



def get_max_freq(magnitude=[],time=[]):
    sample_period = time[1]-time[0]
    n_samples = len(time)
    fft_magnitudes=np.abs(np.fft.fft(magnitude))
    fft_frequencies = np.fft.fftfreq(n_samples, sample_period)
    fft_clean_frequencies_array = []
    for freq in range(len(fft_frequencies)):
        if fft_magnitudes[freq] > 100:
            fft_clean_frequencies_array.append(fft_frequencies[freq])
    max_freq = max(fft_clean_frequencies_array)
    return max_freq


def round_to_nearest(n, m):
    return m * math.ceil(n / m)

def take_samples(time, signal_magnitude, sample_rate):
    step = time[1]-time[0]
    max_freq = get_max_freq(signal_magnitude, time)
    period = 1/max_freq
    df = pd.DataFrame({"time":time, "Amplitude":signal_magnitude})

    #sample_rate = rate * max_freq
    T_sample = 1/sample_rate
    time_array = np.arange(period/4, df['time'].iloc[-1], T_sample)

    sample_amplitude = []

    for value in time_array:
        sample_amplitude.append(df.iloc[int(round(round_to_nearest(value, step),10)/step)]['Amplitude'])
        
    return (time_array  ,  sample_amplitude)

def sinc_interpolation(input_magnitude, input_time, original_time):
    period = input_time[1] - input_time[0]
    sincM = np.tile(original_time, (len(input_time), 1)) - \
        np.tile(input_time[:, np.newaxis], (1, len(original_time)))
    output_magnitude = np.dot(input_magnitude, np.sinc(sincM/period))
    return output_magnitude

    

class tap:
    def __init__(self, magnitude=None, time=None, label=None, source = "generate" , amplitude = 5,frequency=20 ,sampling_rate=2, noise_check_box = False, snr=1000):
        self.label = label
        self.source = source
        self.magnitude = magnitude
        self.time = time
        self.sampling_rate = sampling_rate
        self.noise_check_box = noise_check_box
        self.snr = snr
        self.amplitude = amplitude
        self.frequency = frequency

    def set_attributes(self, magnitude=None, time=None, label=None, source = "generate" , amplitude = 5,frequency=20 ,sampling_rate=2, noise_check_box = False, snr=1000):
        self.label = label
        self.source = source
        self.magnitude = magnitude
        self.time = time
        self.sampling_rate = sampling_rate
        self.noise_check_box = noise_check_box
        self.snr = snr
        self.amplitude = amplitude
        self.frequency = frequency
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

