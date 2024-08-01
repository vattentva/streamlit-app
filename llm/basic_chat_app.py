import streamlit as st
import openai
from config.auth import init_authenticator

if st.secrets["APP_ENV"] == "development":
    st.write(st.session_state)

st.title("ChatGPT-like clone")

authenticator = init_authenticator()
if st.session_state['authentication_status']:
    with st.sidebar:
        st.write(f'ログイン名： *{st.session_state["name"]}*')
        authenticator.logout(button_name='ログアウト')
        st.divider()
else:
    st.write('TODO: 説明文')
    st.page_link("login.py", label="ログインはこちら")

    st.stop()

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("ChatDemoにメッセージを送信する"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant's response in chat message container
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0,
                stream=True,
                stream_options={"include_usage": True}, # retrieving token usage for stream response
            )
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.stop()

        response = st.write_stream(chat_completion)

        # https://cookbook.openai.com/examples/how_to_stream_completions

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
