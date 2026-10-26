import streamlit as st
from pathlib import Path
from config import APP_NAME, HISTORY_LIMIT
from core.memory_manager import MemoryManager
from components.sidebar import render_sidebar
from components.header import render_header
from modules import dashboard, live_monitor, memory_lab, allocation_lab, paging_lab, process_manager, pressure_lab, storage_lab, analytics, reports

st.set_page_config(page_title=APP_NAME,page_icon="◈",layout="wide",initial_sidebar_state="expanded")
css=Path("assets/styles.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>",unsafe_allow_html=True)

def initialize():
    defaults={"memory":MemoryManager(1024),"history":[],"processes":[],"pressure_history":[],"allocation_success":0,"paging_step":0}
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v
initialize()
page,mode=render_sidebar(); render_header(page,mode,page=="Live System Monitor" or mode=="Live System Mode")
dispatch={
    "Performance Dashboard": dashboard.render,
    "Live System Monitor": lambda s,m: live_monitor.render(s),
    "Memory Management Lab": lambda s,m: memory_lab.render(s),
    "Allocation Algorithms": lambda s,m: allocation_lab.render(s),
    "Paging Simulator": lambda s,m: paging_lab.render(s),
    "Process and CPU Lab": lambda s,m: process_manager.render(s),
    "Memory Pressure Lab": lambda s,m: pressure_lab.render(s),
    "Storage and I/O Lab": lambda s,m: storage_lab.render(s),
    "Performance Analytics": lambda s,m: analytics.render(s),
    "Reports and Viva Center": lambda s,m: reports.render(s),
}
dispatch[page](st.session_state,mode)
