from typing import Optional
import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from utils.supabase.SubmitsTable import SubmitsTable
from views.common import app, debug
from config.log import setup

log = setup()
app(title='🦜🔗 Quickstart App')

# openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai_api_key = st.secrets["OPENAI_API_KEY"]

def generate_response(input_text) -> Optional[str]:
    try:
        llm = OpenAI(temperature=0.7, api_key=openai_api_key)
        return llm(input_text)
    except Exception as e:
        st.error('error')
        log.error(e)
    return None

# 例文のリスト
example_prompts = [
    "AIと機械学習の違いについて簡単に説明してください。",
    "リモートワークで生産性を向上させるためのヒントは何ですか？",
    "健康的な食事を維持するための簡単なレシピを教えてください。",
    "初心者向けの簡単なギターの曲を教えてください。",
    "日本の文化について知っておくべき重要な点を教えてください。"
]
# 例文を自動挿入するボタン
for i, prompt in enumerate(example_prompts):
    if st.button(prompt):
        st.session_state.input_text = example_prompts[i]

with st.form('my_form'):
    default_prompt = st.session_state.get('input_text', '')

    text = st.text_area('Enter text:', default_prompt)
    submitted = st.form_submit_button('Submit')

    if submitted:
        response = generate_response(text)
        if response:
            st.markdown(response)

        client = SubmitsTable()
        client.insert_prompt(
            type=1,
            prompt=text,
            response=response,
            user_name=st.session_state["name"],
            is_success=True if response else False
        )

debug()
