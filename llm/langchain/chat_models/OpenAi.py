import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain.callbacks import get_openai_callback
from langchain_community.callbacks.openai_info import OpenAICallbackHandler

class OpenAi:
    def __init__(self, system_message='You are a helpful assistant.'):
        self._system_message = system_message
        self.gpt_models = [
            # 'gpt-4o',
            'gpt-4o-mini',
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
            st.session_state.costs = []

    def select_model(self):
        model = st.sidebar.radio('Choose a model', self.gpt_models)
        
        temperature = st.sidebar.slider(
            'Temperature',
            min_value=0.0,
            max_value=2.0,
            value=0.0,
            step=0.01
        )
        return ChatOpenAI(temperature=temperature, model=model)

    def get_answer(self, llm: ChatOpenAI, messages: list) -> tuple[str, OpenAICallbackHandler]:
        with get_openai_callback() as cb:
            answer = llm(messages)
        return answer.content, cb
