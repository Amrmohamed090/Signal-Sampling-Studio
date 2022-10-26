
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




st.set_page_config(layout="wide")
#Title of the Website
st.markdown("<h2 style='text-align:center; color: white;'>Sampling Studio</h2>", unsafe_allow_html=True)
#Upload file
file = st.file_uploader("Upload Signal", type= ['csv'])
#(18e3th9)remove gap in title, (hxt7ib)remove gap in sidebar, (x8wxsk) style upload button


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
    #st.session_state['composed_signal'] = np.sin(0)
    st.session_state['upload'] = False
    st.session_state['compose'] = False
    

#draw starts      
def draw_signal(f_magnitude=[], f_time=[],initialize=False , draw = True):
    fig = go.Figure()
    
    

    f_magnitude = np.array(f_magnitude)
    f_time = np.array(f_time)
    time_space = np.linspace(f_time[0], f_time[-1], 2000)
    
    if noise_check_box:   
        f_magnitude = add_noise(snr, f_magnitude)

    f_nyquist = 2*get_max_freq(f_magnitude,f_time)
        
    fig.add_trace(go.Line( x=f_time, y=f_magnitude,name="Original"))
    amplitude_time_samples = take_samples(f_time ,f_magnitude ,sampling_rate)
    fig.add_trace(go.Scatter( x=amplitude_time_samples[0], y=amplitude_time_samples[1],name="Samples", mode='markers'))
    magnitude_recovered = sinc_interpolation(amplitude_time_samples[1], amplitude_time_samples[0], time_space)
    
    fig.add_trace(go.Line( x=time_space, y=magnitude_recovered,name="Recovered"))
    fig.update_layout(xaxis_title="Time(sec)",yaxis_title="Amplitude(V)",legend_title=signal_name,font=dict(size=18,))
    st.plotly_chart(fig, use_container_width=True)
    
    
#draw ends
def save_fun():
      #start save action
     if save:        
         if signal_name not in st.session_state["taps_names"]:
             
             st.session_state['taps_names'].append(signal_name)
             st.session_state['count'] +=1
             if file is None:
                 st.session_state['taps'].append(tap(magnitude = generatedsignal,time=time_generated ,amplitude=amplitude, frequency = freq,noise_check_box = noise_check_box, snr=snr,sampling_rate = sampling_rate, label=signal_name))
             if file is not None:
                 st.session_state['taps'].append(tap(magnitude=np.array(data[data.columns[1]]), time = np.array(data[data.columns[0]]),noise_check_box = noise_check_box, source="csv" ,snr=snr,sampling_rate = sampling_rate, label=signal_name))   
         else:
             st.markdown("this name exist, please change the name")              
     #end save action
     return
#Sidebar
with st.sidebar:
     if file is not None:
         st.session_state["upload"] = True

     if file is None:
          st.session_state['upload'] = False

     st.markdown("<h2 style='text-align: left; color: white;'>To generate signal:</h2>", unsafe_allow_html=True)
     amplitude=st.number_input('Enter Amplitude: ', step = 1, min_value=0, value=5,disabled=  st.session_state["upload"])
     freq=st.number_input('Enter Frequence: ', step=1, min_value=0, value=20,disabled=  st.session_state["upload"])
     sampling_rate=st.slider(label="R * fmax" ,min_value=0.25,max_value=10.0,step=0.25,value=2.0)
     with st.container():
                noise_check_box = st.checkbox("add noise")
                if noise_check_box:
                    st.session_state["snr_state"] = False
                else :
                    st.session_state["snr_state"] = True
                snr = st.number_input("SNR", min_value=0, step=1,value=30,disabled=st.session_state["snr_state"])
     signal_name = st.text_input("Name", value = "signal "+str(st.session_state["count"]))
     save = st.button("Save")
     

       
                


if file is not None :
     data = pd.read_csv(file)
     draw_signal(data[data.columns[1]],data[data.columns[0]])
     if save:
         save_fun()


     
     
if file is None :
     time_generated = np.arange(0, 1, 1/2000)
     generatedsignal = amplitude * np.sin(2 * np.pi * freq * time_generated)
     if save:
         save_fun()
     # Compose 
     generated_signals = []
     generated_signals_names = []
     #filtering only the signals that we generated, not the ones that has been uploaded
     for tp in st.session_state['taps']:
         if tp.source == "generate":
             generated_signals.append(tp)
          
     if generated_signals :
         for tp in generated_signals:
             generated_signals_names.append(tp.label)
     with st.sidebar:
        st.markdown("<h2 style='text-align:left; color: white;'>To compose signals:</h2>", unsafe_allow_html=True)   
        chosen_list = st.multiselect("Sum signals",generated_signals_names)

     taps = []
     #draw_signal(initialize=True)
     fig1 = go.Figure()
      
     for label in chosen_list:
         for i in range(len(st.session_state['taps_names'])):
             if label == st.session_state['taps_names'][i]:
                 taps.append(st.session_state['taps'][i])
     for tp in taps:
         fig1.add_trace(go.Line( x= tp.time, y= tp.magnitude,name=tp.label))
     
     time_x= np.arange(0,1,1/2000)
     signals_sum=np.zeros(len(time_x))
     for tp in taps:
         if not len(signals_sum):
             signals_sum = tp.magnitude
             
         else:
             signals_sum += tp.magnitude
                
     if len(chosen_list) > 0:
        fig1.add_trace(go.Line(x=time_x,y=signals_sum,name="Sum Of Signals"))
        fig1.update_layout(xaxis_title="Time(sec)",yaxis_title="Amplitude(V)",legend_title="Compose",font=dict(size=18,))
        st.plotly_chart(fig1, use_container_width=True)

     else:
        draw_signal(generatedsignal,time_generated)

st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
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
            *, ::before, ::after {
                /* box-sizing: border-box; */
            }
            .css-x8wxsk {
                display: flex;
                -webkit-box-align: center;
                align-items: center;
                padding: 0.3rem;
                background-color: rgb(38, 39, 48);
                border-radius: 0.3rem;
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
                width: 21rem;
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

            }

        </style>
        """, unsafe_allow_html=True)