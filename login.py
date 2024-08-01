import streamlit as st
from config.auth import init_authenticator, login_form

if st.secrets["APP_ENV"] == "development":
    st.write(st.session_state)

authenticator = init_authenticator()
login_form(authenticator=authenticator)

if st.session_state['authentication_status']:
    with st.sidebar:
        st.write(f'ログイン名： *{st.session_state["name"]}*')
        authenticator.logout(button_name='ログアウト')
        st.divider()
    st.title('TODO: Some content')
    st.page_link("llm/basic_chat_app.py", label="Chat App Clone")

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
