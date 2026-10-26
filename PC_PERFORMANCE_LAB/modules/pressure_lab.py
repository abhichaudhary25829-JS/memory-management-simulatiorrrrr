import streamlit as st
import pandas as pd
from core.memory_pressure import pressure_level
from components.charts import line_chart

def render(state):
    mem=state["memory"]; snap=mem.snapshot(); level=pressure_level(snap["utilization"])
    st.metric("Current simulated memory pressure",level,f"{snap['utilization']:.1f}% allocation utilization")
    demand=st.number_input("New controlled demand (KB)",1,mem.total,128,key="pressure_demand"); count=st.number_input("Number of requests",1,30,3,key="pressure_count")
    if st.button("Generate pressure requests",key="pressure_run"):
        for i in range(int(count)):
            pid=f"PRESS-{len(mem.events)+i+1}"; ok,msg=mem.allocate(pid,"Pressure workload",int(demand),"First Fit")
            state["pressure_history"].append({"step":len(state["pressure_history"])+1,"utilization":mem.snapshot()["utilization"],"free":mem.free,"result":"allocated" if ok else "failed"})
        st.rerun()
    if st.button("Recover with compaction",key="pressure_compact"): mem.compact(); state["pressure_history"].append({"step":len(state["pressure_history"])+1,"utilization":mem.snapshot()["utilization"],"free":mem.free,"result":"compacted"}); st.success("Free blocks merged; no actual memory was used.")
    if state["pressure_history"]: st.plotly_chart(line_chart(state["pressure_history"],["utilization","free"],"Pressure trend from actual simulator results"),use_container_width=True); st.dataframe(pd.DataFrame(state["pressure_history"]),use_container_width=True,hide_index=True)
    st.info("Failure reasons are recorded in the memory event log: insufficient total memory or no contiguous block large enough. A real PC is never pressured by this lab.")
