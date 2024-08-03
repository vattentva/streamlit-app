import streamlit as st
from langchain.llms import OpenAI
from config.auth import init_authenticator
from views.common import app, debug
from config.log import setup

log = setup()
app(title='🦜🔗 Quickstart App')

# openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai_api_key = st.secrets["OPENAI_API_KEY"]

def generate_response(input_text):
    try:
        llm = OpenAI(temperature=0.7, api_key=openai_api_key)
        st.markdown(llm(input_text))
    except Exception as e:
        st.error('error')
        log.info('='*100)
        log.error(e)
        log.info('='*100)

with st.form('my_form'):
    default_prompt = 'シンギュラリティの到来はいつですか？'
    text = st.text_area('Enter text:', default_prompt)
    submitted = st.form_submit_button('Submit')

    if submitted:
        generate_response(text)

debug()
