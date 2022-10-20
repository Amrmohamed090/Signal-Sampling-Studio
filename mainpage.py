import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import streamlit as st
import pandas as pd
import plotly.express as ff
from streamlit_option_menu import option_menu
import numpy as np
import plotly.graph_objects as go 
from numpy import linspace,cos,pi,ceil,floor,arange
from mpld3 import plugins

 

st.set_page_config(layout="wide")
# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

#Title of the Website
st.markdown("<h1 style='text-align: center; color: white;'>Sampling Studio</h1>", unsafe_allow_html=True)

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

#SideBar Menu
with st.sidebar:
  selected = option_menu(
    menu_title = "Main menu", 
    options = ["Upload Signal", "Generate Signal","Add Signal"],
  )
if selected == "Upload Signal":
  file = st.file_uploader("Upload Signal", type= ['csv'])
  
  if file is None:
    data = pd.DataFrame({"x":[0,0,0],"y":[0,0,0]})
    original_fig = ff.line(data, x=data.columns[0], y=data.columns[1], title="Original signal")
    sampled_fig = ff.line(data, x=data.columns[0], y=data.columns[1], title="Sampled Signal")
    st.plotly_chart(original_fig, use_container_width=True)
    st.plotly_chart(sampled_fig, use_container_width=True)
  
  
  if file is not None:
    data = pd.read_csv(file)
    fig = ff.line(data, x=data.columns[0], y=data.columns[1], title="Original signal")
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    
   #to generate a signal  
if selected == "Generate Signal":
  amplitude=st.number_input('Enter Amplitude: ', step = 1, min_value=0, value=5)
  freq=st.number_input('Enter Frequence: ', step=1, min_value=0, value=20)
   
  time = np.arange(0, 1, 1/1000)
  genratedsignal = amplitude * np.sin(2 * np.pi * freq * time)

  #adding noise to the generated signal
  with st.container():
      noise_check_box = st.checkbox("add noise")
      
      if noise_check_box:
        snr = st.number_input("SNR", min_value=0, step=1,value=30)
        genratedsignal = add_noise(snr, genratedsignal)

  fig = go.Figure()
  fig.add_trace(go.Line( x=time, y=genratedsignal))
  

  # sampling the original signal
  sample_freq=st.slider(label="Sample Rate: Nyquist frequence=" + str(2*freq),min_value=1,max_value=2000,step=1,value=freq*2)
  T = 1/sample_freq
  n = np.arange(0,1/T)
  samples=amplitude * np.sin(2 * np.pi *freq* n*T)
  fig.add_trace(go.Scatter( x=n*T, y=samples, mode='markers'))
  st.plotly_chart(fig, use_container_width=True)
  fig=fig.update_layout(showlegend=True)

  #recovering the signal 

  fig = ff.line(reconstruct(time),title="sampled signal")

  st.plotly_chart(fig, use_container_width=True)  

#Add signals:
if selected == "Add Signal":
  #data of first signal
  col1 , col2 = st.columns(2)
  amplitude1 = col1.number_input('Enter Amplitude for the first signal: ')
  freq1 = col1.number_input('Enter Frequence for the first signal: ')
  time = np.arange(0, 1, 1/1000)
  signal1 = amplitude1 * np.sin(2 * np.pi * freq1 * time)
  df1 = pd.DataFrame({"time":time,"amplitude":signal1})
  fig1 = ff.line(df1, x=df1.columns[0], y=df1.columns[1], title="First signal")
  st.plotly_chart(fig1, use_container_width=True)
  #data of second signal
  amplitude2 = col2.number_input('Enter Amplitude for the second signal: ')
  freq2 = col2.number_input('Enter Frequence for the second signal: ')
  time = np.arange(0, 1, 1/1000)
  signal2 = amplitude2 * np.sin(2 * np.pi * freq2 * time)
  three_subplot_fig = plt.figure(figsize=(10,6))
  df2 = pd.DataFrame({"time":time,"amplitude":signal2})
  fig2 = ff.line(df2, x=df2.columns[0], y=df2.columns[1], title="Second signal")
  st.plotly_chart(fig2, use_container_width=True)

  #adding the two signals
  output_signal = pd.Series.add(df2["amplitude"], df1["amplitude"])
  df3 = pd.DataFrame({"time":time,"amplitude":output_signal})
  fig3 = ff.line(df3, x=df3.columns[0], y=df3.columns[1], title="Output signal")
  st.plotly_chart(fig3, use_container_width=True)
  st.pyplot(three_subplot_fig)








#   T = 1 / freqsample
#   n = np.arange(0, 0.5 / T)
#   nT = n * T
#   time2 = np.arange(-1, 1 + 1/freqsample, 1/freqsample)
#   sampledsignal = amplitude * np.sin(2 * np.pi * freq* time2) # Since for sampling t = nT.
#   fig2 = ff.line(sampledsignal, x=time2,y = sampledsignal)
#   st.plotly_chart(fig2, use_container_width=True)

# arr1 = []
# arr2 = []
# for row in file:
#     arr1.append(row[0])
#     #arr2.append(row[1])    
#     arr1Up = [float(x) for x in arr1]
#     arr2Up = [float(x) for x in arr2]
# st.title('ECG signal')
# fig = plt.figure()
# plt.xlim([0,1])
# plt.xlabel("time")
# plt.ylabel("yaxis")
# plt.ylim([-1,2])
# plt.plot(arr1Up,arr2Up)
# fig_html = mpld3.fig_to_html(fig)
# components.html(fig_html, height=600)
    
# st.pyplot(fig)




