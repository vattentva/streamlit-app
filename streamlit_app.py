import streamlit as st

# カスタムCSSを適用
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    .styles_terminalButton__JBj5T {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# report_1 = st.Page("reports/DataFrame_Demo.py")
# report_2 = st.Page("reports/Mapping_Demo.py")
# report_3 = st.Page("reports/Plotting_Demo.py")

sidebar = {
    "Streamlit": [
        st.Page("login.py", title="Top")
    ],
    "LLM": [
        # st.Page("llm/basic_chat_app.py", title="ChatBot App"),
        # st.Page("llm/langchain_chat_app.py", title="LangChain QuickStart App"),
        st.Page("llm/langchain_openai.py", title="LangChain Chat Model"),
    ],
}
# if st.secrets["APP_ENV"] == "development":
#     sidebar["Admin"] = [
#         st.Page("register.py", title="Register")
#     ]

pg = st.navigation(sidebar)
pg.run()
