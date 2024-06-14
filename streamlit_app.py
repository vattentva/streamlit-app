import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import time, datetime

st.header('st.checkbox')

st.write ('What would you like to order?')

icecream = st.checkbox('Ice cream')
coffee = st.checkbox('Coffee')
cola = st.checkbox('Cola')

if icecream:
     st.write("Great! Here's some more ??")

if coffee: 
     st.write("Okay, here's some coffee ?")

if cola:
     st.write("Here you go ??")

# df2 = pd.DataFrame(
#      np.random.randn(200, 3),
#      columns=['a', 'b', 'c'])
# st.write(df2)
# st.line_chart(df2)


# c = alt.Chart(df2).mark_circle().encode(
#      x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
# st.write(c)

# df3 = pd.read_csv("data.csv")
# st.write(df3)
