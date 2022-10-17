from tkinter import HORIZONTAL
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import numpy as np 


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
st.markdown("<h1 style='text-align: center; color: black;'>Sampling Studio</h1>", unsafe_allow_html=True)

#SideBar Menu
selected = option_menu(
    menu_title = "Main menu", 
    options = ["Sampler", "Composer"],
    icons=["bar-chart-line","activity"],
    orientation=HORIZONTAL
  )
# with st.sidebar:
file = st.file_uploader("Sampler", type= ['csv'])
if file is None:
  st.write("please , upload the signal")
  
  data = pd.DataFrame({"x":[0,0,0],"y":[0,0,0]})
  original_fig = px.line(data, x=data.columns[0], y=data.columns[1], title="Original signal")
  sampled_fig = px.line(data, x=data.columns[0], y=data.columns[1], title="Sampled Signal")
  st.plotly_chart(original_fig, use_container_width=True)
  st.plotly_chart(sampled_fig, use_container_width=True)

if file is not None:
  data = pd.read_csv(file)
  if selected == "Sampler":
      # data = pd.read_csv(file)
      fig = px.line(data, x=data.columns[0], y=data.columns[1], title="Original signal")
      
      sampled_fig = px.scatter(data, x=data.columns[0], y=data.columns[1], title="Sampled Signal")
      st.plotly_chart(fig, use_container_width=True)
      st.plotly_chart(sampled_fig, use_container_width=True)
      
      slider_value=st.slider(label="value",min_value=1,max_value=10,step=1)
      st.write(slider_value)
      
      
  if selected == "Composer":
    #genrate=st.checkbox("Genrate A Signal")

    fig = px.line(data, x=data.columns[0], y=data.columns[1], title="Original signal")
    st.plotly_chart(fig, use_container_width=True)

    amplitude=st.number_input('Enter Amplitude: ')
    freq=st.number_input('Enter Frequence: ')
    sampling_freq = 500
    time = np.arange(-1, 1 + 1/sampling_freq, 1/sampling_freq)
    theta=st.number_input('Enter phase: ')
    generatedsignal = amplitude * np.sin(2 * np.pi * freq * time + theta)
    #composed signal= original signal+generated signal
    fig = px.line(generatedsignal , x=time, y=generatedsignal, title="Composed Signal")
    st.plotly_chart(fig, use_container_width=True)
    
    
    

    


