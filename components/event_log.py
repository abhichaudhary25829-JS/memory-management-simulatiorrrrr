import streamlit as st
def render_events(events):
    if not events: st.info("No simulation events recorded yet."); return
    for e in events[-8:][::-1]: st.caption(f"• {e['event']} — Used {e['used']} KB, Free {e['free']} KB")
