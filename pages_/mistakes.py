import streamlit as st
from components import render_mistakes


def app() -> None:
    st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Mistakes</h1>", unsafe_allow_html=True)

    render_mistakes()
