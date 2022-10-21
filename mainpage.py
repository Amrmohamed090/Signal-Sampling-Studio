import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, magnitude_spectrum
import streamlit as st
import pandas as pd
import plotly.express as ff
from streamlit_option_menu import option_menu
import numpy as np
import plotly.graph_objects as go 
import math
from tkinter import HORIZONTAL
from resources import *


st.set_page_config(layout="wide")
# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 1.3rem;
                    padding-bottom: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
                ::-webkit-scrollbar {
                    background: transparent;
                    border-radius: 100px;
                    height: 3px;
                    width: 1px;
                }
        </style>
        """, unsafe_allow_html=True)
#Title of the Website
#st.markdown("<h1 style='text-align: center; color: white;'>Sampling Studio</h1>", unsafe_allow_html=True)
#SideBar Menu
selected = option_menu(
    menu_title = "Sampling Studio",
    options = ["Sampler", "Generate","Composer"],
    icons=["bar-chart-line","activity"],
    orientation=HORIZONTAL
  )


#SideBar Menu
with st.sidebar:
  pass
  ###################################################################################################################################################
if selected == "Sampler":
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
    f_nyquist = 2*get_max_freq(data[data.columns[1]],data[data.columns[0]])
    sampling_rate=st.slider(label="Sample Rate: Nyquist frequence=" + str(round(f_nyquist,4)),min_value=0.25,max_value=10.0,step=0.25,value=2.0)
    time_amplitude_samples = take_samples(data[data.columns[0]],data[data.columns[1]],sampling_rate)
    fig.add_trace(go.Scatter( x=time_amplitude_samples[0], y=time_amplitude_samples[1], mode='markers'))
    st.plotly_chart(fig, use_container_width=True)
    
    
  ##############################################################################################################################################################
    
   #to generate a signal  
if selected == "Generate":
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
  f_nyquist = 2*get_max_freq(genratedsignal,time)
  sampling_rate=st.slider(label="Sample Rate: Nyquist frequence=" + str(round(f_nyquist , 4)),min_value=0.25,max_value=10.0,step=0.25,value=2.0)
  amplitude_time_samples = take_samples(time,genratedsignal,sampling_rate)
  """
  T = 1/sample_freq
  n = np.arange(0,1/T)
  samples=amplitude * np.sin(2 * np.pi *freq* n*T)
  """
  fig.add_trace(go.Scatter( x=amplitude_time_samples[0], y=amplitude_time_samples[1], mode='markers'))
  st.plotly_chart(fig, use_container_width=True)
  fig=fig.update_layout(showlegend=True)

  #recovering the signal 

  magnitude_revovered = sinc_interpolation(amplitude_time_samples[1], amplitude_time_samples[0], time)
  df2 = pd.DataFrame({"time":time,"amplitude":magnitude_revovered})
  fig2 = ff.line(df2, x=df2.columns[0], y=df2.columns[1], title="Recovered signal")
  st.plotly_chart(fig2, use_container_width=True)  

############################################################################################################################################
#Add signals:
if selected == "Composer":
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
#adding Buttons
col1 , col2 = st.columns(2)
with col1:
    st.button('Save')
with col2:
    st.button('Delete')





