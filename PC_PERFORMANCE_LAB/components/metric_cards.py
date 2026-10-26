import streamlit as st
def metrics(items):
    cols=st.columns(len(items))
    for col,(label,value,detail) in zip(cols,items):
        with col: st.metric(label,value,detail)
