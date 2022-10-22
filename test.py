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

if 'taps' not in st.session_state:
    st.session_state['taps'] = list()
    st.session_state['current_tap'] = 0

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
    selected = option_menu(
        menu_title = "Options",
        options = ["Upload New Signal", "Generate New Signal"],
        icons=["bar-chart-line","activity"],
        orientation=HORIZONTAL
    )
    if selected == "Upload New Signal":
        file = st.file_uploader("Upload Signal", type= ['csv'])
            
            
    if selected == "Generate New Signal":
        amplitude=st.number_input('Enter Amplitude: ', step = 1, min_value=0, value=5)
        freq=st.number_input('Enter Frequence: ', step=1, min_value=0, value=20)
    
    if selected == "Generate New Signal" or (selected == "Upload New Signal" and file is not None) :
        with st.container():
                noise_check_box = st.checkbox("add noise")
                if noise_check_box:
                    snr = st.number_input("SNR", min_value=0, step=1,value=30)
        sampling_rate=st.slider(label="Sample Rate" ,min_value=0.25,max_value=10.0,step=0.25,value=2.0)
        save = st.button("save")





        
def draw_signal(magnitude=[], time=[],initialize=False):
    if initialize:
        fig = go.Figure()
        fig.add_trace(go.Line( x=[0,0,0], y=[0,0,0]))
        st.plotly_chart(fig, use_container_width=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Line( x=[0,0,0], y=[0,0,0]))
        st.plotly_chart(fig2, use_container_width=True)
        return
    magnitude = np.array(magnitude)
    time = np.array(time)
    fig = go.Figure()
    time_space = np.linspace(time[0], time[-1], 1000)
    
    if noise_check_box:   
        magnitude = add_noise(snr, magnitude)

    f_nyquist = 2*get_max_freq(magnitude,time)
    with st.sidebar:
        st.markdown("F nyquist = " + str(round(f_nyquist,5)))
    fig.add_trace(go.Line( x=time, y=magnitude))
    amplitude_time_samples = take_samples(time ,magnitude ,sampling_rate)
    fig.add_trace(go.Scatter( x=amplitude_time_samples[0], y=amplitude_time_samples[1], mode='markers'))

    st.plotly_chart(fig, use_container_width=True)

    magnitude_revovered = sinc_interpolation(amplitude_time_samples[1], amplitude_time_samples[0], time_space)

    fig2 = go.Figure()
    fig2.add_trace(go.Line( x=time_space, y=magnitude_revovered))
    st.plotly_chart(fig2, use_container_width=True)


if selected == "Upload New Signal":

    if file is None:
        draw_signal(initialize=True)


    if file is not None:
        data = pd.read_csv(file)
        draw_signal(data[data.columns[1]],data[data.columns[0]])

   

if selected == "Generate New Signal":

    time = np.arange(0, 1, 1/1000)
    generatedsignal = amplitude * np.sin(2 * np.pi * freq * time)

    #adding noise to the generated signal

    draw_signal(generatedsignal,time)
    
     

