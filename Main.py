from msilib.schema import Icon
from turtle import fillcolor
from requests import session
import streamlit as st
import pandas as pd
import plotly.express as ff
from streamlit_option_menu import option_menu
import numpy as np
import plotly.graph_objects as go 
import math
from tkinter import HORIZONTAL
from resources import *




st.set_page_config(page_title = "Sampling Studio", layout="wide")

#Upload file
file = st.file_uploader("Upload Signal", type= ['csv'])
time_generated = np.arange(0, 1, 1/2000)
fig = go.Figure()

if 'time_init' not in st.session_state:
    st.session_state['time_init'] = [0,0]
    st.session_state['magnitude_init'] = [0,0]
    st.session_state['taps'] = list()
    st.session_state['taps_names'] = list()
    st.session_state['curr_tap'] = None
    st.session_state['count'] = 1
    st.session_state['snr_state'] = True
    st.session_state['save_flag'] = False
    st.session_state['compose_list'] = list()
    st.session_state['upload'] = False
    st.session_state['compose'] = False
    st.session_state['table']=[]
    st.session_state['freq_mag']=[]
    
def max_freq():
    if len(st.session_state["table"])==0:
        maxfreq=0
    else:
        maxfreq=max(st.session_state["table"])
    return maxfreq 
#draw starts      
def draw_signal(f_magnitude=[], f_time=[],sampling_rate=1,initialize=False, draw = True):

    f_magnitude = np.array(f_magnitude)
    f_time = np.array(f_time)
    time_space = np.linspace(1/(get_max_freq(f_magnitude,f_time)*4), f_time[-1], 2000)
    if noise_check_box:   
        f_magnitude = add_noise(snr, f_magnitude)

        
    if samplingFreq_checkBox:
        sampling_rate=sampling_method
    else:
        sampling_rate=sampling_method*max_freq()

    amplitude_time_samples = take_samples(f_time ,f_magnitude ,sampling_rate)
    magnitude_recovered = sinc_interpolation(amplitude_time_samples[1], amplitude_time_samples[0], time_space)   
    if initialize:
      fig.add_trace(go.Scatter( x=amplitude_time_samples[0], y=amplitude_time_samples[1],name="Samples", mode='markers'))
      fig.add_trace(go.Line( x=f_time, y=f_magnitude,name="Original"))
      fig.add_trace(go.Line( x=time_space, y=magnitude_recovered,name="Recovered"))
      fig.update_layout(xaxis_title="Time(sec)",yaxis_title="Amplitude(V)",legend_title="SIGNALS",font=dict(size=18))
    
    if draw:
      fig.add_trace(go.Scatter( x=amplitude_time_samples[0], y=amplitude_time_samples[1],name="Samples", mode='markers'))
      fig.add_trace(go.Line( x=f_time, y=f_magnitude,name="Original"))
      fig.add_trace(go.Line( x=time_space, y=magnitude_recovered,name="Recovered"))
      fig.update_layout(xaxis_title="Time(sec)",yaxis_title="Amplitude(V)",legend_title="SIGNALS",font=dict(size=18))
      
    if not draw:
       return (time_space,magnitude_recovered)
#draw ends

def save_fun():
     
      #start save action     
     if signal_name not in st.session_state["taps_names"]:
         st.session_state['taps_names'].append(signal_name)
         st.session_state['count'] +=1
         if file is None:
             saved_signal_T,saved_signal_M= draw_signal(generatedsignal,time_generated, draw=False)
             st.session_state['taps'].append(tap(magnitude = saved_signal_M,time=saved_signal_T ,amplitude=amplitude, frequency = freq,noise_check_box = noise_check_box, snr=snr, label=signal_name))
         if file is not None:
             saved_signal_T,saved_signal_M=draw_signal(data[data.columns[1]],data[data.columns[0]], draw=False)
             st.session_state['taps'].append(tap(magnitude=saved_signal_M, time = saved_signal_T,noise_check_box = noise_check_box, source="csv" ,snr=snr, label=signal_name))  
     else:
         st.warning("This name exist, please change the name")              
     #end save action
     return

def add_fun():
    signals_sum=np.zeros(len(time_generated))
    for tp in st.session_state["taps"]:
                 signals_sum += tp.magnitude
    return signals_sum
    
#Sidebar
with st.sidebar:
    #  if file is not None:
        #  st.session_state["upload"] = True

    #  if file is None:
        #   st.session_state['upload'] = False


     col3,col4=st.sidebar.columns(2)
     with st.container():
        freq=col3.number_input('Frequency ', step=1, min_value=1, value=20)
        amplitude=col4.number_input('Amplitude ', step = 1, min_value=1, value=5)
        generatedsignal=amplitude * np.sin(2 * np.pi * freq * time_generated)
        
        
     samplingFreq_checkBox= st.checkbox("Sampling by Frequency")
     if samplingFreq_checkBox:
        sampling_method = st.slider("Sampling Frequency",min_value=2,max_value=800,value=2)
        
     else:
        sampling_method=st.slider(label="Normalized Frequency" ,min_value=1,max_value=10,step=1,value=2)
     with st.container():
                st.markdown("<div style='margin-top:-12%; margin-buttom:-12%;'><hr color='white'></div>",unsafe_allow_html=True)
                noise_check_box = st.checkbox("Add Noise")
                if noise_check_box:
                    st.session_state["snr_state"] = False
                else :
                    st.session_state["snr_state"] = True
                snr = st.number_input("SNR", min_value=1, step=1,value=30,disabled=st.session_state["snr_state"])
     st.markdown("<div style='margin-top:-12%; margin-buttom:-12%;'><hr color='white'></div>",unsafe_allow_html=True)
     signal_name = st.text_input("Name", value = "signal "+str(st.session_state["count"]))
     col1,col2=st.sidebar.columns(2)
     add = col1.button("Add")
                
if file is not None :
     data = pd.read_csv(file)
     generatedsignal=data[data.columns[1]]
     if add:
         save_fun()
         st.session_state['compose'] = True    
     if st.session_state['compose']:
          generatedsignal=add_fun()
          
     draw_signal(generatedsignal,data[data.columns[0]],sampling_method,draw=True)
     recoveredsignal = draw_signal(data[data.columns[1]],data[data.columns[0]], draw = False)
     downloadedsignal = pd.DataFrame({"time":recoveredsignal[0],"magnitude":recoveredsignal[1]})
     with st.sidebar:
         col2.download_button(
            label="Download",
            data=convert_df_to_csv(downloadedsignal),
            file_name='your_signal.csv',
            mime='text/csv',
            )
         

if file is None :
    st.session_state['table'].append(freq)
    
    if add:
         save_fun()
         st.session_state['table'].append(freq)
         st.session_state['freq_mag'].append([freq,amplitude])
         st.session_state['compose'] = True
         
    if st.session_state['compose']:
         generatedsignal=add_fun()
         
                 
    
    chosen_list = st.sidebar.multiselect("Remove Signals",st.session_state['freq_mag'])
    remove=st.sidebar.button("Remove")
    if remove:
         for item in chosen_list:
             for tp in st.session_state['taps']:
                 if item[0] == tp.frequency and item[1]==tp.amplitude:
                      st.session_state["taps"].remove(tp)
             
                      
             for item2 in st.session_state['freq_mag']:
                 if item == item2:
                     st.session_state['freq_mag'].remove(item2)
     
     
             for item3 in st.session_state['table']:
                 if item[1] == item3:
                     st.session_state['table'].remove(item3)        
         st.experimental_rerun()
              
    draw_signal(generatedsignal,time_generated,sampling_method,initialize=True,draw=False)
    recoveredsignal = draw_signal(generatedsignal,time_generated, draw = False)     
    downloadedsignal = pd.DataFrame({"time":recoveredsignal[0],"magnitude":recoveredsignal[1]})
    
    with st.sidebar:        
        col2.download_button(
           label="Download",
           data=convert_df_to_csv(downloadedsignal),
           file_name='your_signal.csv',
           mime='text/csv',
           )
# if compose_signal:
#      if add:
#          save_fun()
#                   # Compose 
#      generated_signals = []
#      generated_signals_names = []
#      for tp in st.session_state['taps']:
#           generated_signals.append(tp)
#      if generated_signals :
#          for tp in generated_signals:
#              generated_signals_names.append(tp.label)
#      with st.sidebar:
#          st.markdown("<div style='margin-top:-10%; margin-buttom:-50%;'><hr color='white'></div>",unsafe_allow_html=True)
#          #compose_button = st.checkbox("Compose")
#          chosen_list = st.multiselect("Remove Signals",generated_signals_names, disabled=not compose_signal)
#      taps = []
#      labels = []
#      for label in chosen_list:
#          
#                  taps.append(st.session_state['taps'][i])
#                  labels.append(label)
#      signals_sum=np.zeros(len(time_generated))
     
#      if add:           
#          draw_signal(signals_sum,time_generated,draw=True)

#if add:
#     save_fun()
#     updated_signal=np.zeros(len(time_generated))
#     for tp in st.session_state['taps']:
#         updated_signal += tp.magnitude
#     draw_signal(updated_signal,time_generated,sampling_method,draw=True) 
     

     
     
     
     
     
     


# if add:
    # save_fun()
# Compose 
# generated_signals = []
# generated_signals_names = []
# signals_sum=np.zeros(len(time_x))
# for tp in st.session_state['taps']:
    #  signals_sum += tp.magnitude
     
# if generated_signals :
#     for tp in generated_signals:
#         generated_signals_names.append(tp.label)
# with st.sidebar:
#    st.markdown("<div style='margin-top:-10%; margin-buttom:-10%;'><hr color='white'></div>",unsafe_allow_html=True)
#    chosen_list = st.multiselect("Compose Signals",generated_signals_names)
#taps = []

 
# for label in chosen_list:
#     for i in range(len(st.session_state['taps_names'])):
#         if label == st.session_state['taps_names'][i]:
#             taps.append(st.session_state['taps'][i])


# time_x= np.arange(0,1,1/2000)
# signals_sum=np.zeros(len(time_x))
# for tp in taps:
#         signals_sum += tp.magnitude
          
# if len(chosen_list) > 0:
#    fig = go.Figure()
#    fig.add_trace(go.Line(x=time_x,y=signals_sum))
#    fig.update_layout(xaxis_title="Time(sec)",yaxis_title="Amplitude(V)",title="Sum Of Signals",font=dict(size=18))
 
   
st.plotly_chart(fig, use_container_width=True)

 
#
st.markdown("""
        <style>

            .css-18e3th9 {
                flex: 1 1 0%;
                width: 100%;
                padding: 1.4rem 10rem 18rem;
                min-width: auto;
                max-width: initial;
            }
            .css-hxt7ib {
                padding-top: 1rem; 
                padding-left: 1rem;
                padding-right: 1rem;
            }
            ::-webkit-scrollbar {
                background: transparent;
                border-radius: 100px;
                height: 4px;
                width: 10px;
            }
            .css-x8wxsk {
                display: flex;
                -webkit-box-align: center;
                align-items: center;
                padding: 0.3rem;
                background-color: rgb(38, 39, 48);
                border-radius: 0.8rem;
                color: rgb(250, 250, 250);
            }
            .css-1adrfps {
                background-color: rgb(240, 242, 246);
                background-attachment: fixed;
                flex-shrink: 0;
                height: calc(-2px + 100vh);
                top: 2px;
                overflow: auto;
                padding: .5rem .5rem;
                position: relative;
                transition: margin-left 300ms ease 0s, box-shadow 300ms ease 0s;
                width: 50rem;
                z-index: 1000021;
                margin-left: 0px;
                }
            .e16nr0p30{
                    -webkit-user-select: none;  /* Chrome all / Safari all */
                    -moz-user-select: none;     /* Firefox all */
                    -ms-user-select: none;      /* IE 10+ */
                    user-select: none;          /* Likely future */     
            
            }
            .effi0qh3{
                -webkit-user-select: none;  /* Chrome all / Safari all */
                    -moz-user-select: none;     /* Firefox all */
                    -ms-user-select: none;      /* IE 10+ */
                    user-select: none;          /* Likely future */ 
            }
            .e16nr0p33{
                -webkit-user-select: none;  /* Chrome all / Safari all */
                    -moz-user-select: none;     /* Firefox all */
                    -ms-user-select: none;      /* IE 10+ */
                    user-select: none;          /* Likely future */ 
            }
            .exg6vvm12{
                -webkit-user-select: none;  /* Chrome all / Safari all */
                    -moz-user-select: none;     /* Firefox all */
                    -ms-user-select: none;      /* IE 10+ */
                    user-select: none;          /* Likely future */ 

            }
            .e88czh80{
                -webkit-user-select: none;  /* Chrome all / Safari all */
                    -moz-user-select: none;     /* Firefox all */
                    -ms-user-select: none;      /* IE 10+ */
                    user-select: none;          /* Likely future */ 
            .css-16huue1 {
                  font-size: 18px;
                  color: rgb(250, 250, 250);
                  margin-bottom: 7px;
                  height: auto;
                  min-height: 1.5rem;
                  vertical-align: middle;
                  display: flex;
                  flex-direction: row;
                  -moz-box-align: center;
                  align-items: center;
            }
            .css-3snfz0 {
                   font-size: 18px;
                   color: rgba(250, 250, 250, 0.4);
                   margin-bottom: 7px;
                   height: auto;
                   min-height: 1.5rem;
                   vertical-align: middle;
                   display: flex;
                   flex-direction: row;
                   -moz-box-align: center;
                   align-items: center;
            }
            .css-1oe6wy4 h2 {
                  font-size: 1.5rem;
                  font-weight: 600;
            }
 
        
            .css-ocqkz7.e1tzin5v4 {
                display: flex;
                flex-wrap: wrap;
                -webkit-box-flex: 1;
                flex-grow: 1;
                -webkit-box-align: stretch;
                align-items: stretch;
                gap: 1rem;
                background-color:#484848;
                align-items: center;
                boarder-radius:2%;
                }
         

        </style>
        """, unsafe_allow_html=True)