import streamlit as st
from utils.supabase.SubmitsTable import SubmitsTable
from views.common import app, debug
from config.log import setup
from llm.langchain.chat_models.OpenAi import OpenAi

# from langchain.llms import OpenAI
# from langchain_openai import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain.callbacks import get_openai_callback

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

    client.insert_prompt(
        type=2,
        prompt=user_input,
        response=answer,
        user_name=st.session_state["name"],
        is_success=True if answer else False,
        total_cost=handler.total_cost,
        prompt_tokens=handler.prompt_tokens,
        completion_tokens=handler.completion_tokens,
    )

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
