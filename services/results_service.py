import streamlit as st

from services.base_service import BaseService


class ResultsService(BaseService):
    prefix: str = "results"

    def reasons(self):
        endpoint = "reasons"

        @st.cache_data(ttl=120)
        def fetch_cached_data():
            return self.fetch_data(endpoint)

        return fetch_cached_data()
