import streamlit as st
from config.auth import init_authenticator, login_form

def app(title='', top=False):
    st.title(title)

    authenticator = init_authenticator()
    if st.session_state['authentication_status']:
        if top:
            st.page_link("llm/basic_chat_app.py", label="Chat App Clone")
            st.page_link("llm/langchain_chat_app.py", label="Langchain QuickStart")
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
    if st.secrets["APP_ENV"] == "development":
        st.write(st.session_state)
