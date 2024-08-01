import streamlit as st

# report_1 = st.Page("reports/DataFrame_Demo.py")
# report_2 = st.Page("reports/Mapping_Demo.py")
# report_3 = st.Page("reports/Plotting_Demo.py")

# tool_1 = st.Page("page_1.py", title="CSVデータ可視化くん", icon=":material/add_circle:")

# auth_1 = st.Page("auth_step1.py", title="Auth Intro")
# auth_2 = st.Page("auth_step2.py", title="User & Password")

llm1 = st.Page("llm/basic_chat_app.py", title="Chat Demo")
login = st.Page("login.py", title="Login")

pg = st.navigation(
    {
        "LLM": [llm1],
        # "Reports": [report_1, report_2, report_3],
        # "Tools": [tool_1],
        # "Auth": [auth_1, auth_2],
        "Streamlit Auth": [login],
        # "Transformers": [tf_1],
    }
)
pg.run()
