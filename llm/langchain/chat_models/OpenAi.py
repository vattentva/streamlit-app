import streamlit as st

from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain_community.chat_models import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from langchain_community.callbacks.openai_info import OpenAICallbackHandler

from utils import const

class OpenAi:
    def __init__(self, system_message=const.LangchainConfig.SYSTEM_MESSAGE.value):
        self._system_message = system_message
        self.gpt_models = [
            'gpt-4o-mini',
            # 'gpt-4o',
            # 'gpt-3.5-turbo'
        ]

    def init_message(self):
        clear_button = st.sidebar.button("履歴をクリア", key="clear")
        
        # チャット履歴の初期化
        # del st.session_state.messages
        if clear_button or "messages" not in st.session_state:
            st.session_state.messages = [
                SystemMessage(content=self._system_message)
            ]

    def select_model(self):
        model = st.sidebar.radio('GPT Model', self.gpt_models)
        
        temperature = st.sidebar.slider('Temperature',
            min_value=0.0, max_value=2.0,
            value=0.0, step=0.01
        )
        return ChatOpenAI(temperature=temperature, model=model)

    def get_answer(self, llm: ChatOpenAI, messages: list) -> tuple[str, OpenAICallbackHandler]:
        with get_openai_callback() as cb_handler:
            answer = llm(messages)
        return answer.content, cb_handler
