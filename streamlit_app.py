import streamlit as st

# report_1 = st.Page("reports/DataFrame_Demo.py")
# report_2 = st.Page("reports/Mapping_Demo.py")
# report_3 = st.Page("reports/Plotting_Demo.py")

# top = st.Page("login.py", title="Top")
# llm1 = st.Page("llm/basic_chat_app.py", title="ChatBot App")
# llm2 = st.Page("llm/langchain_chat_app.py", title="LangChain QuickStart App")
# llm3 = st.Page("llm/langchain_openai.py", title="LangChain OpenAI")

sidebar = {
    "Streamlit": [
        st.Page("login.py", title="Top")
    ],
    "LLM": [
        st.Page("llm/basic_chat_app.py", title="ChatBot App"),
        st.Page("llm/langchain_chat_app.py", title="LangChain QuickStart App"),
        st.Page("llm/langchain_openai.py", title="LangChain OpenAI"),
    ],
}
# if st.secrets["APP_ENV"] == "development":
#     sidebar["Admin"] = [
#         st.Page("register.py", title="Register")
#     ]

pg = st.navigation(sidebar)
pg.run()
