import streamlit as st
import subprocess
import os
import sys
# Get the absolute path to the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)



st.set_page_config(
    page_title="Use",
    page_icon="📖",
    layout="wide"
)

st.markdown(
        "<style>#MainMenu{visibility:hidden;}</style>",
        unsafe_allow_html=True
)
# st.header("Geometry parameters")
# Get the session state for osmode
#osmode = st.session_state.osmode

tab1, tab2 = st.tabs(["Prompts", "Advanced"])
#tab1
with tab1:
    st.markdown("#Prompts the model")

#tab2
with tab2:
    pass
