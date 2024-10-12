import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

from pages_ import logins
from services.logins_service import LoginsService


def main():
    st.set_page_config(page_title="ANALYTICS", layout="wide", page_icon="🔥")

    if "credentials" not in st.session_state:
        logins_service = LoginsService()
        st.session_state.credentials = logins_service.credentials()

    authenticator = stauth.Authenticate(
        credentials=st.session_state.credentials,
        cookie_name="cookies_name",
        cookie_key="cookies_key",
        cookie_expiry_days=30.0
    )

    name, state, username = authenticator.login()

    if state:
        if "rerun" not in st.session_state:
            st.session_state.rerun = True
            st.rerun()

        name = st.session_state.credentials['usernames'][username]['name']

        with st.sidebar:

            options = [
                "Logins"
            ]
            icons = [
                "bi bi-key"
            ]

            selected = option_menu(
                menu_title="Navigation",
                options=options,
                icons=icons
            )

            st.subheader(f"Welcome, :violet[{name.capitalize()}]\n")

        if selected == "Logins":
            logins.app()

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')

    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


if __name__ == "__main__":
    main()
