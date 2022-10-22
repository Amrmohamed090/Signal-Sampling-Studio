import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, magnitude_spectrum
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
    st.session_state['composed_signal'] = np.sin(0)

    
    

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
                iframe {
                    border: none;
                    padding: 0px;
                    margin-top: 23px;
                    }
        </style>
        """, unsafe_allow_html=True)
#Title of the Website
#st.markdown("<h1 style='text-align: center; color: white;'>Sampling Studio</h1>", unsafe_allow_html=True)
#SideBar Menu

with st.sidebar:
    main_menu = option_menu(
            menu_title = "Main Menu",
            options = ["Add Signal", "Choose Signal"] ,
            icons=["bar-chart-line","activity"],
            orientation=HORIZONTAL
    )
if main_menu == "Add Signal":
    with st.sidebar:
        
        selected = option_menu(
            menu_title = "Options",
            options = ["Upload Signal", "Generate Signal", "Compose Signals"],
            icons=["bar-chart-line","activity"],
            orientation=HORIZONTAL
        )
        if selected == "Upload Signal":
            file = st.file_uploader("Upload Signal", type= ['csv'])
            if file is not None:
                data = pd.read_csv(file)    
                
        if selected == "Generate Signal":
            amplitude=st.number_input('Enter Amplitude: ', step = 1, min_value=0, value=5)
            freq=st.number_input('Enter Frequence: ', step=1, min_value=0, value=20)
            time_generated = np.arange(0, 1, 1/1000)
            generatedsignal = amplitude * np.sin(2 * np.pi * freq * time_generated)
        
        if selected == "Generate Signal" or (selected == "Upload Signal" and file is not None) :
            with st.container():
                    noise_check_box = st.checkbox("add noise")
                    if noise_check_box:
                        st.session_state["snr_state"] = False
                    snr = st.number_input("SNR", min_value=0, step=1,value=30,disabled=st.session_state["snr_state"])
                    
            sampling_rate=st.slider(label="R * fmax" ,min_value=0.25,max_value=10.0,step=0.25,value=2.0)
            signal_name = st.text_input("Name", value = "signal "+str(st.session_state["count"]))
            save = st.button("save")
           
           #start save action
            if save:        
                if signal_name not in st.session_state["taps_names"]:
                    
                    st.session_state['taps_names'].append(signal_name)
                    st.session_state['count'] +=1
                    if selected == "Generate Signal":
                        st.session_state['taps'].append(tap(magnitude = generatedsignal,time=time_generated ,amplitude=amplitude, frequency = freq,noise_check_box = noise_check_box, snr=snr,sampling_rate = sampling_rate, label=signal_name))
                    if selected == "Upload Signal":
                        st.session_state['taps'].append(tap(magnitude=np.array(data[data.columns[1]]), time = np.array(data[data.columns[0]]),noise_check_box = noise_check_box, source="csv" ,snr=snr,sampling_rate = sampling_rate, label=signal_name))
                        
            #end save action            
                        


                else:
                    st.markdown("this name exist, please change the name")


                    
            
            





#draw starts      
def draw_signal(f_magnitude=[], f_time=[],initialize=False):
    if initialize:
        fig = go.Figure()
        fig.add_trace(go.Line( x=st.session_state["time_init"], y=st.session_state["magnitude_init"]))
        st.plotly_chart(fig, use_container_width=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Line(  x=st.session_state["time_init"], y=st.session_state["magnitude_init"]))
        st.plotly_chart(fig2, use_container_width=True)
        return
    f_magnitude = np.array(f_magnitude)
    f_time = np.array(f_time)
    fig = go.Figure()
    time_space = np.linspace(f_time[0], f_time[-1], 1000)
    
    if noise_check_box:   
        f_magnitude = add_noise(snr, f_magnitude)

    f_nyquist = 2*get_max_freq(f_magnitude,f_time)
    with st.sidebar:
        st.markdown("F nyquist = " + str(round(f_nyquist,5)))
    fig.add_trace(go.Line( x=f_time, y=f_magnitude))
    amplitude_time_samples = take_samples(f_time ,f_magnitude ,sampling_rate)
    fig.add_trace(go.Scatter( x=amplitude_time_samples[0], y=amplitude_time_samples[1], mode='markers'))

    
    
    magnitude_recovered = sinc_interpolation(amplitude_time_samples[1], amplitude_time_samples[0], time_space)

    fig2 = go.Figure()
    fig2.add_trace(go.Line( x=time_space, y=magnitude_recovered))
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
#draw ends


if main_menu == "Choose Signal" and st.session_state["taps_names"]:
    with st.sidebar:
        selected = option_menu(
        menu_title = "Signals",
        options =st.session_state["taps_names"],
        icons=["activity"]
        )
    for i in range(len(st.session_state["taps_names"])):
        if selected == st.session_state["taps_names"][i]:
            st.session_state['curr_tap'] = i
            break
    curr_tap = st.session_state['taps'][st.session_state['curr_tap']]
    
    with st.sidebar:
        
        noise_check_box = st.checkbox("add noise", value = curr_tap.noise_check_box)
        if noise_check_box:
            st.session_state["snr_state"] = False
        snr = st.number_input("SNR", min_value=0, step=1,value=curr_tap.snr,disabled=st.session_state["snr_state"])
        sampling_rate=st.slider(label="R * fmax" ,min_value=0.25,max_value=10.0,step=0.25,value=float(curr_tap.sampling_rate))
        
        

        if curr_tap.source == "csv":
            time = curr_tap.time
            magnitude = curr_tap.magnitude
            
            

        if curr_tap.source == "generate":
            amplitude=st.number_input('Enter Amplitude: ', step = 1, min_value=0, value=curr_tap.amplitude)
            freq=st.number_input('Enter Frequence: ', step=1, min_value=0, value=curr_tap.frequency)
            time = np.arange(0, 1, 1/1000)
            magnitude = amplitude * np.sin(2 * np.pi * freq * time)
            
            #adding noise to the generated signal
        
        signal_name = st.text_input("Name", value = "signal"+str(st.session_state["count"]))
        save = st.button("save")
        if save:
            if signal_name not in st.session_state.taps_names:
                if curr_tap.source == "generate":
                        curr_tap.set_attributes(label=signal_name, magnitude=magnitude,time=time,amplitude=amplitude, frequency = freq,noise_check_box = noise_check_box, snr=snr,sampling_rate = sampling_rate)
                if curr_tap.source == "csv":
                        curr_tap.set_attributes(time = curr_tap.time, label=signal_name, magnitude = curr_tap.magnitude,noise_check_box = noise_check_box, source="csv" ,snr=snr,sampling_rate = sampling_rate)
        
            else:
                st.markdown("this name exists!! please try another name")
    
    draw_signal(magnitude,time)
        
            





if main_menu == "Add Signal":
    if selected == "Upload Signal":

        if file is None:
            draw_signal(initialize=True)


        if file is not None:
            
            draw_signal(data[data.columns[1]],data[data.columns[0]])

    

    if selected == "Generate Signal":
        
        #adding noise to the generated signal
        draw_signal(generatedsignal,time_generated)
    
    if selected == "Compose Signals":
        
        generated_signals = []
        #filtering only the signals that we generated, not the ones that has been uploaded
        for tap in st.session_state['taps']:
            if tap.source == "generate":
                generated_signals.append(tap)
        
        if generated_signals :
            generated_signals_names = []
            for tap in generated_signals:
                generated_signals_names.append(tap.label)
                    
            with st.sidebar:        
                chosen_list = st.multiselect("Added signals",generated_signals_names)
            
            taps = []

            for label in chosen_list:
                for i in range(len(st.session_state['taps_names'])):
                    if label == st.session_state['taps_names'][i]:
                        taps.append(st.session_state['taps'][i])
            sum=list()
            fig1 = go.Figure()
            for tap in taps:
                fig1.add_trace(go.Line( x= tap.time, y= tap.magnitude))
                if not len(sum):
                    sum = tap.magnitude
                else:
                    sum += tap.magnitude
            x= np.arange(0,1,1/1000) 
            fig2 = go.Figure()
            fig2.add_trace(go.Line( x=x, y=sum))
            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)
         
                    
        
        else:
            draw_signal(initialize=True)
           



     


    
    
    
    