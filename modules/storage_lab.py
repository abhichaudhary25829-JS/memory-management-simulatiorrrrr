import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.disk_scheduler import disk_schedule
from components.metric_cards import metrics

def render(state):
    st.caption("Simulated disk head scheduling; this is separate from live disk I/O telemetry.")
    req=st.text_input("Cylinder requests", "98,183,37,122,14,124,65,67",key="disk_req"); head=st.number_input("Initial head",0,999,53,key="disk_head"); size=st.number_input("Disk cylinders",10,10000,200,key="disk_size"); algo=st.selectbox("Disk scheduling",["FCFS","SSTF","SCAN","C-SCAN","LOOK","C-LOOK"],key="disk_algo"); direction=st.radio("Scan direction",["up","down"],horizontal=True,key="disk_direction")
    if st.button("Calculate head movement",key="disk_run"):
        try: state["disk_result"]=disk_schedule([int(x.strip()) for x in req.split(',') if x.strip()],int(head),int(size),algo,direction)
        except ValueError as e: st.error(str(e))
    r=state.get("disk_result")
    if r:
        metrics([("Total movement",f"{r['movement']} cylinders","head travel"),("Average seek",f"{r['average_seek']:.2f}","cylinders/request"),("Service count",len(r['order']),"requests"),("Algorithm",r['algorithm'],"simulation")]); st.write("Service order:"," → ".join(map(str,r["order"])))
        fig=go.Figure(go.Scatter(x=list(range(len(r["path"]))),y=r["path"],mode="lines+markers",line=dict(color="#25c7d9"))); fig.update_layout(template="plotly_dark",title="Disk head movement path",xaxis_title="Step",yaxis_title="Cylinder",height=330); st.plotly_chart(fig,use_container_width=True)
