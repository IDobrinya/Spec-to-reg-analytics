import pandas as pd
import streamlit as st
from requests import RequestException
from streamlit_authenticator.utilities.hasher import Hasher

from services.logins_service import LoginsService

logins_service = LoginsService()


def render_logins(commit_button, rollback_button):
    if "credentials" not in st.session_state:
        st.session_state.credentials = logins_service.credentials()

    if rollback_button:
        st.session_state.credentials = logins_service.credentials()

    credentials = st.session_state.credentials

    users_data = []
    for username, details in credentials['usernames'].items():
        users_data.append({
            'username': username,
            'name': details['name'],
            'password': details['password']
        })

    df = pd.DataFrame(users_data)

    col1, col2 = st.columns([3, 1])
    with col1:
        edited_df = st.data_editor(df, num_rows="dynamic", key="user_editor", hide_index=True)
    with col2:
        st.write("ℹ :violet[Usernames] must be unique")
        st.write("ℹ :red[Never] change username of logged in user")

    if commit_button:
        edited_passwords = edited_df['password']
        idx = []
        passwords_to_hash = []
        for i, passwrd in enumerate(edited_passwords):
            if passwrd not in list(df['password']):
                idx.append(i)
                passwords_to_hash.append(passwrd)

        hashed_passwords = Hasher(passwords_to_hash).generate()
        for i, hashed_password in zip(idx, hashed_passwords):
            edited_passwords[i] = hashed_password

        new_usernames = set(edited_df['username'])
        old_usernames = set(df['username'])

        for username, name, hashed_password, role in zip(edited_df['username'], edited_df['name'], edited_passwords, edited_df['role']):
            credentials['usernames'][username] = {
                        'name': name,
                        'password': hashed_password
                    }

        removed_users = old_usernames - new_usernames
        for username in removed_users:
            del credentials['usernames'][username]

        try:
            response = logins_service.commit_credentials(credentials)
        except RequestException as e:
            st.error(f"Post error. {e}")
            return
        if response.get("status") == "success":
            st.success(response.get("message"))
            st.session_state.credentials = logins_service.credentials()
        else:
            st.error(response.get("message"))
            st.session_state.credentials = logins_service.credentials()
