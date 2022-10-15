import streamlit as st
import pandas as pd
import plotly.express as ff
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
st.markdown("<h1 style='text-align: center; color: white;'>Sampling Studio</h1>", unsafe_allow_html=True)

#SideBar Menu
with st.sidebar:
  selected = option_menu(
    menu_title = "Main menu", 
    options = ["Upload Signal", "Generate Signal"],
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
    
    
if selected == "Generate Signal":
  #genrate=st.checkbox("Genrate A Signal")
  amplitude=st.number_input('Enter Amplitude: ')
  freq=st.number_input('Enter Frequence: ')
  sampling_freq = 500
  time = np.arange(-1, 1 + 1/sampling_freq, 1/sampling_freq)
  theta=st.number_input('Enter phase: ')
  genratedsignal = amplitude * np.sin(2 * np.pi * freq * time + theta)
  fig = ff.line(genratedsignal, x=time, y=genratedsignal)
  st.plotly_chart(fig, use_container_width=True)



