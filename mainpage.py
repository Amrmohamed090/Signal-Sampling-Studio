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
  amplitude=st.number_input('Enter Amplitude: ')
  freq=st.number_input('Enter Frequence: ')
  time = np.arange(0, 1, 1/1000)
  genratedsignal = amplitude * np.sin(2 * np.pi * freq * time)
  fig = go.Figure()
  fig.add_trace(go.Line( x=time, y=genratedsignal))
  

  # sampling the original signal
  sample_freq=st.slider(label="sample rate",min_value=1,max_value=1000,step=1)
  T = 1/sample_freq
  n = np.arange(0,1/T)
  samples=amplitude * np.sin(2 * np.pi *freq* n*T)
  fig.add_trace(go.Scatter( x=n*T, y=samples, mode='markers'))
  st.plotly_chart(fig, use_container_width=True)
  fig=fig.update_layout(showlegend=True)

  #recovering the signal 
  def reconstruct(time):
      sum=0
      for i in range(-sample_freq, sample_freq, 1):
          #signal=amplitude * np.sin(2 * np.pi *freq* i*T)
          sum += genratedsignal*np.sinc((time- i*T)/T) 
      return sum

  fig = ff.line(reconstruct(time),title="sampled signal")
  st.plotly_chart(fig, use_container_width=True)  

#Add signals:
#data of first signal
amplitude1 = st.number_input('Enter Amplitude for the first signal: ')
freq1 = st.number_input('Enter Frequence for the first signal: ')
time = np.arange(0, 1, 1/1000)
signal1 = amplitude1 * np.sin(2 * np.pi * freq1 * time)
#data of second signal
amplitude2 = st.number_input('Enter Amplitude for the second signal: ')
freq2 = st.number_input('Enter Frequence for the second signal: ')
time = np.arange(0, 1, 1/1000)
signal2 = amplitude2 * np.sin(2 * np.pi * freq2 * time)
three_subplot_fig = plt.figure(figsize=(10,6))
plt.subplot(311)
plt.plot(time, signal1, color='tab:blue')


plt.subplot(312)
plt.plot(time, signal2, color='black')
plt.subplot(313)
plt.plot(time, signal1+signal2, color='red')

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




