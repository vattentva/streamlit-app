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
st.sidebar.title("Options")

# カウントの最大値を設定
MAX_CALLS = 5
# セッションの初期化
if "call_count" not in st.session_state:
    st.session_state.call_count = 0

chat_model = OpenAi()
chat_model.init_message()
llm = chat_model.select_model()

# ユーザーの入力を監視
user_input = st.chat_input("メッセージを送信する")
st.markdown('**回答は必ずしも正しいとは限りません。重要な情報は確認するようにしてください。**')
if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.spinner("ChatGPT is typing ..."):
        answer, handler = chat_model.get_answer(llm, st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=answer))
    st.session_state.costs.append(handler.total_cost)

    client = SubmitsTable()
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

    st.session_state.call_count += 1

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

costs = st.session_state.get('costs', [])
st.sidebar.markdown("## Costs")
st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
for cost in costs:
    st.sidebar.markdown(f"- ${cost:.5f}")

# カウントの表示
st.sidebar.write(f"Usage: {st.session_state.call_count} / {MAX_CALLS}")

debug()
