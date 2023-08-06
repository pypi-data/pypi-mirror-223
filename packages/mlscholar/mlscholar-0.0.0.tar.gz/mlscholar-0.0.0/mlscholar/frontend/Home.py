import streamlit as st
import os

st.set_page_config(
    page_title="MLscholar",
    page_icon="📖",
    layout="centered"
)
#pulsars version
pulsars_v = "(v0.0.0)"


# st.sidebar.image('../../assets/logo.png', use_column_width=True)
# Main Description
home_title = "📖 MLscholar 📖"
home_subtitle = " Search, explore and use ML models..."
st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>{pulsars_v}</font></span>""", unsafe_allow_html=True)

st.markdown(
    f"""<div style="background-color: #ECF4FF; padding: 10px; border-radius: 5px;">
        <h1 style="color: #01205F; font-size: 3px;"><span style="font-size: 18px;">{home_subtitle}</span>
    </div>""",
    unsafe_allow_html=True
)

# Add a horizontal line to simulate a separator
st.markdown('<hr style="border-top: 2px solid #01205F;">', unsafe_allow_html=True)
st.markdown("#### Welcome")
st.markdown("Author : __Damien Sicard__: https://github.com/altar31")
st.markdown("The app is still under heavy development. Please reach me if you have any comments or suggestions.")

# Description of the features.
st.markdown(
    """
    - **Search** : this is the ML models search engine.
    - **Use** :  a system for load and use pre-trained models.
    - **Build** : an integrated model builder.
    """
)

# st.markdown('<hr style="border-top: 2px solid #01205F;">', unsafe_allow_html=True)
st.markdown("##### Operating system")
osmode = st.radio("Please select an operating system", ('Windows', 'Linux'))
st.caption("You selected " + osmode)

