import streamlit as st
import pandas as pd
from components.charts import line_chart, bar
from core.allocation_algorithms import compare_algorithms
from core.paging_engine import simulate_replacement

def render(state):
    st.caption("Every chart below is based on recorded telemetry or results produced by a simulator engine in this session.")
    history=state["history"]
    if history:
        st.plotly_chart(line_chart(history,["cpu","ram","swap","disk"],"Recorded performance measurements"),use_container_width=True)
    else: st.info("Visit the Performance Dashboard to collect session measurements.")
    alloc=state.get("allocation_comparison")
    if alloc:
        df=pd.DataFrame(alloc); st.subheader("Allocation algorithms"); st.plotly_chart(bar(df,"algorithm","external_fragmentation","External fragmentation (KB)"),use_container_width=True)
    page_data=[]
    for algo in ["FIFO","LRU","Optimal"]:
        r=simulate_replacement([7,0,1,2,0,3,0,4,2,3,0,3,2],3,algo); page_data.append({"algorithm":algo,"page_faults":r["faults"],"page_hits":r["hits"]})
    st.subheader("Page-replacement comparison — fixed educational sequence"); st.dataframe(pd.DataFrame(page_data),hide_index=True,use_container_width=True); st.plotly_chart(bar(pd.DataFrame(page_data),"algorithm","page_faults","Calculated page faults"),use_container_width=True)
    if state.get("disk_result"): st.info(f"Latest disk experiment: {state['disk_result']['algorithm']} travelled {state['disk_result']['movement']} cylinders.")
