import logging
import streamlit as st
from llm.langchain.chat_models.OpenAi import OpenAi
from utils import const
from utils.supabase.SubmitsTable import SubmitsTable
from views.common import app, debug

from typing import Optional
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

app(title='Website Summarize')
client = SubmitsTable()

container = st.container()
response_container = st.container()

def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_content(url: str) -> Optional[str]:
    try:
        with st.spinner("Fetching Content ..."):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # st.info([soup.main, soup.article, soup.body.get_text()])
            # fetch text from main (change the below code to filter page)
            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            else:
                return soup.body.get_text()
    except Exception as e:
        logging.error(e)
        st.error('URL PARSE ERROR')
        return None

def build_prompt(content, n_chars=300):
    return f"""以下はとあるWebページのコンテンツである。内容を{n_chars}文字程度でわかりやすく要約してください。

========

{content[:1000]}

========

日本語で書いてね！
"""

model = OpenAi()
llm = model.select_model()

answer = None

with container:
    if url := st.text_input("URL: "):
        is_valid_url = validate_url(url)
        if not is_valid_url:
            st.info('Please input valid url')
        else:
            content = get_content(url)
            if content:
                prompt = build_prompt(content)
                st.session_state.messages.append(HumanMessage(content=prompt))
                with st.spinner("ChatGPT is typing ..."):
                    answer, handler = model.get_answer(llm, st.session_state.messages)
                    client.logging_request(const.RequestType.SUMMARY.value, prompt, answer, handler)

        # session meesages clearing
        st.session_state.messages = [
            SystemMessage(content=const.LangchainConfig.SYSTEM_MESSAGE.value)
        ]

if answer:
    with response_container:
        st.markdown("## Summary")
        st.write(answer)
        st.markdown("---")
        st.markdown("## Original Text")
        st.write(content)

model.init_message()

debug()
