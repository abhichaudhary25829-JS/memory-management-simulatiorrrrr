import io, json
import streamlit as st
import pandas as pd
from utils.session_manager import load_session
from utils.report_generator import summary_pdf

def _download(label, rows, filename):
    if rows: st.download_button(label,pd.DataFrame(rows).to_csv(index=False).encode(),file_name=filename,mime="text/csv")

def render(state):
    st.subheader("Export calculated results")
    _download("Download performance history CSV",state["history"],"performance_history.csv")
    _download("Download allocation CSV",state.get("allocation_result",{}).get("results",[]),"allocation_results.csv")
    _download("Download paging CSV",state.get("paging_result",{}).get("steps",[]),"paging_results.csv")
    _download("Download scheduling CSV",state.get("schedule_result",{}).get("rows",[]),"scheduling_results.csv")
    latest=state["history"][-1] if state["history"] else {}
    pdf=summary_pdf([
        ("Recorded samples",len(state["history"])),
        ("Latest CPU utilization",f"{latest.get('cpu','Unavailable')}%"),
        ("Latest RAM utilization",f"{latest.get('ram','Unavailable')}%"),
        ("Memory allocation utilization",f"{state['memory'].snapshot()['utilization']:.1f}%"),
        ("Simulated process count",len(state["processes"])),
        ("Paging faults",state.get("paging_result",{}).get("faults","No run recorded")),
        ("Disk movement",state.get("disk_result",{}).get("movement","No run recorded")),
    ])
    st.download_button("Download analytics summary PDF",pdf,"pc_performance_summary.pdf","application/pdf")
    if st.button("Prepare session JSON",key="report_json"):
        export={"history":state["history"],"memory":state["memory"].snapshot(),"processes":state["processes"],"allocation":state.get("allocation_result"),"paging":state.get("paging_result"),"scheduling":state.get("schedule_result"),"disk":state.get("disk_result")}; state["session_json"]=json.dumps(export,indent=2,default=str)
    if state.get("session_json"): st.download_button("Download session JSON",state["session_json"],"pc_performance_lab_session.json","application/json")
    uploaded=st.file_uploader("Load a saved JSON session",type="json")
    if uploaded and st.button("Load session data",key="load_session"):
        try:
            payload=load_session(uploaded); state["history"]=payload.get("history",[]); state["processes"]=payload.get("processes",[]); st.success("History and process records restored. Reinitialize memory if you need to reproduce its exact layout.")
        except (ValueError,json.JSONDecodeError): st.error("This is not a valid PC Performance Lab session JSON.")
    st.divider(); st.subheader("Viva center")
    topics={"Core definitions":"CPU utilization is busy time ÷ elapsed time. RAM holds active data; virtual memory uses disk-backed swap when RAM is insufficient.","Fragmentation":"Internal fragmentation is unused capacity inside an allocated fixed block. External fragmentation is free memory split into separate blocks.","Allocation algorithms":"First Fit picks the first suitable block; Best Fit the smallest suitable; Worst Fit the largest suitable; Next Fit continues searching from the previous placement.","Paging":"A page is a fixed-size logical-memory unit. A page fault occurs when a referenced page is not resident in a physical frame. FIFO evicts oldest, LRU least recently used, and Optimal farthest future use.","CPU scheduling":"FCFS serves arrival order. SJF chooses shortest burst. Priority chooses smallest priority number. Round Robin rotates time slices for fairness.","Disk scheduling":"FCFS serves queue order; SSTF selects nearest request; SCAN sweeps to an edge; LOOK reverses at the last pending request."}
    for heading,text in topics.items():
        with st.expander(heading): st.write(text)
    st.markdown("**Demonstration flow:** collect live telemetry → allocate/deallocate simulated memory → compare allocation algorithms → step through page faults → schedule processes → compare disk head movement → export a session report.")
