import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import hmac

def use_one_global_password():
    def check_password():
        """Returns `True` if the user had the correct password."""

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password.
            else:
                st.session_state["password_correct"] = False

        # Return True if the password is validated.
        if st.session_state.get("password_correct", False):
            st.success('successfully login!', icon="✅")
            return True

        # Show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        if "password_correct" in st.session_state:
            st.error("😕 Password incorrect")
        return False

    if not check_password():
        st.stop()  # Do not continue if check_password is not True.

def auth_view():
    authenticator = init_authenticator()
    authenticator.login(location='sidebar')
    
    if st.session_state["authentication_status"]:
        ## ログイン成功
        with st.sidebar:
            st.markdown(f'## Welcome *{st.session_state["name"]}*')
            authenticator.logout('Logout', 'sidebar')
            st.divider()
        # st.success('successfully login!', icon="✅")

    elif st.session_state["authentication_status"] is False:
        ## ログイン成功ログイン失敗
        st.error('Username/password is incorrect')
        st.stop()

    elif st.session_state["authentication_status"] is None:
        ## デフォルト
        st.warning('Please enter your username and password')
        st.stop()

def login_form(authenticator: stauth.Authenticate):
    return authenticator.login(fields={
        'Form name':'ログイン',
        'Username': 'ユーザー名',
        'Password': 'パスワード',
        'Login': 'ログイン'
    })

def init_authenticator() -> stauth.Authenticate:
    yaml_path = "config.yaml"
    with open(yaml_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Pre-hashing all plain text passwords once
    # Hasher.hash_passwords(config['credentials'])

    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized'],
    )