import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

## ユーザー設定読み込み
yaml_path = "/mount/src/streamlit/LCB_HTML/config.yaml"

with open(yaml_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
)

## UI 
authenticator.login()
if st.session_state["authentication_status"]:
    ## ログイン成功
    with st.sidebar:
        st.markdown(f'## Welcome *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()
    st.write('# ログインしました!')
    
    # HTML埋め込み
    st.markdown("""
        <style>
        .my-text {
            color: white;
            font-size: 24px;
            background-color: #008080;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        <p class='my-text'>Hello World!</p>
        """, unsafe_allow_html=True)

elif st.session_state["authentication_status"] is False:
    ## ログイン成功ログイン失敗
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    ## デフォルト
    st.warning('Please enter your username and password')
