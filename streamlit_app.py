import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader
# from config.logging import setup

yaml_path = "users.yaml"
with open(yaml_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
)

authenticator.login(location='sidebar')
if st.session_state["authentication_status"]:
    ## ログイン成功
    with st.sidebar:
        st.markdown(f'## Welcome *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()
    st.success('successfully login!', icon="✅")

elif st.session_state["authentication_status"] is False:
    ## ログイン成功ログイン失敗
    st.error('Username/password is incorrect')
    # st.stop()

elif st.session_state["authentication_status"] is None:
    ## デフォルト
    st.warning('Please enter your username and password')


with st.sidebar:
    st.write(st.session_state)

# @st.cache_resource
# def main():
#     setup()

# if __name__ == '__main__':
#     main()
