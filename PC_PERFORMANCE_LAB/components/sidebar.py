import streamlit as st
from config import PAGES
def render_sidebar():
    with st.sidebar:
        st.markdown("<div class='brand'>◈ PC PERFORMANCE<br><span>LABORATORY</span></div>",unsafe_allow_html=True)
        page=st.radio("Navigation",PAGES,label_visibility="collapsed")
        st.divider(); mode=st.selectbox("Monitoring mode",["Learning Mode","Live System Mode"])
        st.caption("Live measurements are read-only via psutil. Simulations never consume real RAM or CPU.")
    return page,mode
