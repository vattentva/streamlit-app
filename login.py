import streamlit as st
from config.auth import init_authenticator, login_form
from views.common import app, debug

app(title='Welcome', top=True)

debug()
