import streamlit as st
from config.auth import init_authenticator, login_form

def app(title='', top=False):
    st.title(title)

    authenticator = init_authenticator()
    if st.session_state['authentication_status']:
        if top:
            pages = [
                { 'path': 'llm/langchain_openai.py', 'label': 'LangChain Chat Model'},
                { 'path': 'llm/website_summarize.py', 'label': 'Website Summarize'},
            ]
            for page in pages:
                st.page_link(page['path'], label=page['label'])

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
