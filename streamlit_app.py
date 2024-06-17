import streamlit as st
import pandas as pd
import numpy as np
from config.logging import setup

@st.cache_resource
def init():
    setup()

def show():
    st.title("ホーム")
    st.write("サイドバーからページを選択してください。")

    st.latex(r'''
     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
     \sum_{k=0}^{n-1} ar^k =
     a \left(\frac{1-r^{n}}{1-r}\right)
     ''')

init()
show()
