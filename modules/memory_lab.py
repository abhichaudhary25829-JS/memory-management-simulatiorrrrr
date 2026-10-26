import streamlit as st
import pandas as pd
from core.memory_manager import MemoryManager
from components.memory_visualizer import render_memory
from components.event_log import render_events
from components.metric_cards import metrics

def render(state):
    mem=state["memory"]
    with st.expander("Initialize or reset simulated memory",expanded=False):
        total=st.number_input("Total simulated memory (KB)",64,65536,int(mem.total),key="mem_total")
        parts=st.text_input("Optional partition sizes (comma-separated KB)",key="mem_parts",placeholder="e.g. 256, 256, 512")
        if st.button("Initialize memory",key="mem_init"):
            try: state["memory"]=MemoryManager(total,[int(x.strip()) for x in parts.split(',') if x.strip()] or None); st.rerun()
            except ValueError as e: st.error(str(e))
    mem=state["memory"]; snap=mem.snapshot(); metrics([("Total memory",f"{snap['total']} KB","simulated"),("Allocated",f"{snap['used']} KB",f"{snap['utilization']:.1f}% utilization"),("Free memory",f"{snap['free']} KB","contiguous blocks"),("External fragmentation",f"{snap['external_fragmentation']} KB","free except largest block")])
    st.subheader("Horizontal memory map"); render_memory(snap["blocks"],snap["total"])
    with st.form("memory_allocate"):
        a,b,c,d=st.columns(4); pid=a.text_input("Process ID"); name=b.text_input("Process name"); size=c.number_input("Request (KB)",1,65536,64); strategy=d.selectbox("Placement",["First Fit","Best Fit","Worst Fit"])
        submitted=st.form_submit_button("Allocate process")
    if submitted:
        try:
            ok,msg=mem.allocate(pid,name,int(size),strategy)
            st.success(f"Allocated in block {msg.block_id}.") if ok else st.warning(msg)
        except ValueError as e: st.error(str(e))
    x,y=st.columns(2)
    with x:
        release=st.text_input("Process ID to deallocate",key="mem_release")
        if st.button("Release memory",key="mem_free"):
            try: mem.deallocate(release); st.success("Process memory released.")
            except ValueError as e: st.error(str(e))
    with y:
        if st.button("Compact free space",key="mem_compact"): mem.compact(); st.success("Compaction completed.")
    st.dataframe(pd.DataFrame(mem.snapshot()["blocks"]),use_container_width=True,hide_index=True)
    st.caption("Formulas: Used = Σ allocated block sizes · Free = Σ free block sizes · Internal fragmentation = Σ(block size − request) · External fragmentation = total free − largest free block · Utilization = used ÷ total × 100")
    st.subheader("Allocation event history"); render_events(mem.events)
