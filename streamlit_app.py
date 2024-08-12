import streamlit as st

# カスタムCSSを適用
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

sidebar = {
    "Streamlit": [
        st.Page("login.py", title="Top")
    ],
    "LLM": [
        # st.Page("llm/basic_chat_app.py", title="ChatBot App"),
        # st.Page("llm/langchain_chat_app.py", title="LangChain QuickStart App"),
        st.Page("llm/langchain_openai.py", title="LangChain Chat Model"),
        st.Page("llm/website_summarize.py", title="Website Summarize"),
    ],
}

pg = st.navigation(sidebar)
pg.run()
