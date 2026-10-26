import streamlit as st
import pandas as pd
from utils.system_monitor import snapshot, partitions, top_processes
from components.metric_cards import metrics
from components.charts import bar

def render(state):
    if st.button("Refresh live measurements",key="live_refresh"): state["live"] = snapshot()
    d=state.get("live") or snapshot(); state["live"]=d
    st.info("All values below are live, read-only system measurements collected via psutil. Unsupported sensors are shown as unavailable.")
    metrics([("Total CPU",f"{d['cpu']:.1f}%",f"{d['frequency_mhz'] or 'Unavailable'} MHz"),("RAM",f"{d['ram_percent']:.1f}%",f"{d['ram_available_mb']:.0f} MB available"),("Swap",f"{d['swap_percent']:.1f}%",f"{d['swap_used_mb']:.0f} MB used"),("Processes",d['process_count'],"running / accessible")])
    st.subheader("CPU usage per core"); st.plotly_chart(bar(pd.DataFrame({"Core":[f"CPU {i}" for i in range(len(d['per_cpu']))],"Usage %":d['per_cpu']}),"Core","Usage %"),use_container_width=True)
    st.subheader("Disk partitions"); st.dataframe(pd.DataFrame(partitions()),use_container_width=True,hide_index=True)
    st.caption(f"Disk I/O since boot — Read: {d['disk_read_mb'] if d['disk_read_mb'] is not None else 'Unavailable'} MB · Write: {d['disk_write_mb'] if d['disk_write_mb'] is not None else 'Unavailable'} MB · Network sent/received: {d['net_sent_mb'] if d['net_sent_mb'] is not None else 'Unavailable'} / {d['net_recv_mb'] if d['net_recv_mb'] is not None else 'Unavailable'} MB")
    left,right=st.columns(2)
    with left: st.subheader("Top processes by CPU"); st.dataframe(pd.DataFrame(top_processes("cpu")),use_container_width=True,hide_index=True)
    with right: st.subheader("Top processes by memory"); st.dataframe(pd.DataFrame(top_processes("memory")),use_container_width=True,hide_index=True)
