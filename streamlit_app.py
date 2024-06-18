import streamlit as st
import pandas as pd
import numpy as np
from config.logging import setup
import os

@st.cache_resource
def init():
    setup()

def show():
    st.title('Customizing the theme of Streamlit apps')

    st.write('Contents of the `.streamlit/config.toml` file of this app')

    st.code("""
    [theme]
    primaryColor="#F39C12"
    backgroundColor="#2E86C1"
    secondaryBackgroundColor="#AED6F1"
    textColor="#FFFFFF"
    font="monospace"
    """)

    number = st.sidebar.slider('Select a number:', 0, 10, 5)
    st.write('Selected number from slider widget is:', number)

    # Everything is accessible via the st.secrets dict:
    st.write("DB username:", st.secrets["db_username"])
    st.write("DB password:", st.secrets["db_password"])
    st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

    # And the root-level secrets are also accessible as environment variables:
    st.write(
        "Has environment variables been set:",
        os.environ["db_username"] == st.secrets["db_username"],
    )

init()
show()
