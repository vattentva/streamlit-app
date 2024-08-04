import streamlit as st
from langchain.llms import OpenAI
from utils.supabase.SubmitsTable import SubmitsTable
from views.common import app, debug
from config.log import setup

log = setup()
app(title='🦜🔗 Quickstart App')

# openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai_api_key = st.secrets["OPENAI_API_KEY"]

def generate_response(input_text) -> bool:
    try:
        llm = OpenAI(temperature=0.7, api_key=openai_api_key)
        st.markdown(llm(input_text))
        return True
    except Exception as e:
        st.error('error')
        log.error(e)
    return False

with st.form('my_form'):
    default_prompt = 'シンギュラリティの到来はいつですか？'
    text = st.text_area('Enter text:', default_prompt)
    submitted = st.form_submit_button('Submit')

    if submitted:
        is_success = generate_response(text)

        client = SubmitsTable()
        client.insert_prompt(
            type=1,
            prompt=text,
            user_name=st.session_state["name"],
            is_success=is_success
        )

debug()
