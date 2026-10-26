import streamlit as st
from components.metric_cards import metrics
from components.charts import line_chart, bar
from core.performance_engine import health_status
from utils.system_monitor import snapshot

def render(state, mode):
    live=mode=="Live System Mode"; data=snapshot() if live else {"cpu":state.get("sim_cpu",32),"ram_percent":state.get("memory").snapshot()["utilization"],"swap_percent":4,"frequency_mhz":3200,"logical_cores":8,"physical_cores":4,"ram_total_mb":8192,"ram_used_mb":state.get("memory").used/1024,"ram_available_mb":8192-state.get("memory").used/1024,"disk_percent":41,"process_count":len(state.get("processes",[])),"disk_read_mb":0,"disk_write_mb":0}
    state["history"].append({"cpu":data["cpu"],"ram":data["ram_percent"],"swap":data["swap_percent"],"disk":data.get("disk_percent") or 0,"mode":"live" if live else "simulation"})
    state["history"]=state["history"][-120:]; health,reason=health_status(data["cpu"],data["ram_percent"],data["swap_percent"])
    metrics([("CPU utilization",f"{data['cpu']:.1f}%",f"{data.get('frequency_mhz') or 'N/A'} MHz"),("RAM utilization",f"{data['ram_percent']:.1f}%",f"{data['ram_used_mb']:.0f} MB used"),("Swap / virtual",f"{data['swap_percent']:.1f}%","read-only metric"),("System health",health,reason)])
    st.caption("Source: " + ("actual computer telemetry collected read-only through psutil" if live else "controlled values from this application’s simulation engines"))
    a,b=st.columns(2); a.plotly_chart(line_chart(state["history"],["cpu","ram","swap"],"Utilization history (%)"),use_container_width=True); b.plotly_chart(line_chart(state["history"],["disk"],"Disk utilization (%)"),use_container_width=True)
    st.subheader("System overview")
    metrics([("CPU topology",f"{data.get('physical_cores','—')}P / {data.get('logical_cores','—')}L","physical / logical"),("Active processes",data.get("process_count","—"),"observed or simulated"),("Disk utilization",f"{data.get('disk_percent') or 0:.1f}%","system partition"),("Allocation success",f"{state.get('allocation_success',0):.0f}%","current experiment")])
