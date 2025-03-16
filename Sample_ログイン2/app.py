import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('/mount/src/streamlit/Sample_ログイン2/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'ようこそ *{st.session_state["name"]}* さん')
    st.title('コンテンツ')
elif st.session_state['authentication_status'] is False:
    st.error('ユーザー名またはパスワードが正しくありません')
elif st.session_state['authentication_status'] is None:
    st.warning('ユーザー名とパスワードを入力してください')