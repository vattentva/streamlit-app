import streamlit as st
from config.auth import init_authenticator, login_form
from utils import const

def app(title='', top=False):
    st.title(title)

    authenticator = init_authenticator()
    if st.session_state['authentication_status']:
        if top:
            for page in const.LLM_PAGES:
                st.page_link(page['path'], label=page['title'])

        with st.sidebar:
            st.write(f'User name: *{st.session_state["name"]}*')
            authenticator.logout(button_name='ログアウト')
            st.divider()
    else:
        if top:
            login_form(authenticator=authenticator)
        else:
            st.write("""こちらの機能を利用するにはログインが必要です。""")
            st.page_link("login.py", label="ログインページへ")
            st.stop()

def debug():
    if st.secrets.get('APP_ENV', '') == "development":
        st.write(st.session_state)
