import streamlit as st


st.set_page_config(
    page_title="PID Tuner",
)

st.write("# Welcome to PID Tuner App")

st.markdown(
    """
    PID Tuner is an open-source tool for tuning PID controllers based on historical open-loop data, applying automatic 
    control theory. 
    
    Select "Always rerun" in top right corner!


    ### Created by [NosterDream](https://github.com/nosterdream)
"""
)
