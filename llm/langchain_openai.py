import streamlit as st
from utils import const
from utils.supabase.SubmitsTable import SubmitsTable
from views.common import app, debug
from config.log import setup
from llm.langchain.chat_models.OpenAi import OpenAi

from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

app(title='LangChain Model Chat')
st.markdown('**回答は必ずしも正しいとは限りません。重要な情報は確認するようにしてください。**')
st.sidebar.title("Options")

client = SubmitsTable()

# API呼び出しの最大値を設定
MAX_CALLS = st.secrets.get('MAX_CALLS', 5)
today_call_count = client.select_usage_count()
st.write(f"Usage: {today_call_count} / {MAX_CALLS}")
if today_call_count > MAX_CALLS:
    st.info("使用回数が制限を超えました。")
    st.stop()

chat_model = OpenAi()
llm = chat_model.select_model()

# ユーザーの入力を監視
if user_input := st.chat_input("メッセージを送信する"):
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.spinner("chat model is typing ..."):
        answer, handler = chat_model.get_answer(llm, st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=answer))

    client.logging_request(const.RequestType.CHAT.value, user_input, answer, handler)

    today_call_count = client.select_usage_count()

# チャット履歴の表示
messages = st.session_state.get('messages', [])
for message in messages:
    if isinstance(message, AIMessage):
        with st.chat_message('assistant'):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message('user'):
            st.markdown(message.content)
    # else:  # isinstance(message, SystemMessage):
    #     st.write(f"System message: {message.content}")

chat_model.init_message()

debug()
