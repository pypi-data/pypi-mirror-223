import subprocess
import os
import pandas as pd
import streamlit as st
from contents.dataUI import upload,data_table

# Get the absolute path to the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)

st.set_page_config(
    page_title="MLscholar",
    page_icon="📖",
    layout="wide"
)
# st.markdown(
#         "<style>#MainMenu{visibility:hidden;}</style>",
#         unsafe_allow_html=True
# )
# Get the session state for osmode
#osmode = st.session_state.osmode

tab1, tab2, tab3 = st.tabs(["Data", "Model", "Training"])

#data
with tab1:
    
    uploaded_file = upload()
    data_table(uploaded_file)
#model
with tab2:
    pass
#training
with tab3:
    pass

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)