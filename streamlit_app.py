import streamlit as st

from utils import const

# カスタムCSSを適用
hide_streamlit_style = """
<style>
.stActionButton {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

sidebar = {
    "Streamlit": [
        st.Page("login.py", title="Top")
    ],
    "LLM": [st.Page(page['path'], title=page['title']) for page in const.LLM_PAGES],
}

pg = st.navigation(sidebar)
pg.run()
