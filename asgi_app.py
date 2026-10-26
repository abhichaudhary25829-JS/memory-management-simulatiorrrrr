from pathlib import Path

import streamlit as st


app = st.App(str(Path(__file__).with_name("app.py")))