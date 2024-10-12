import streamlit as st
from components.logins_components import render_logins


def app() -> None:
    col1, col2 = st.columns(2)

    with col1:
        st.title("Logins")
    with col2:
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            rollback_button = st.button("Rollback/Refresh")
        with subcol2:
            commit_button = st.button("Commit Changes")

    render_logins(commit_button, rollback_button)

