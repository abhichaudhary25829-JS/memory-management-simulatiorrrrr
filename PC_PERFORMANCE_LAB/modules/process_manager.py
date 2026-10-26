import streamlit as st
import pandas as pd
import plotly.express as px
from core.process_scheduler import schedule
from components.metric_cards import metrics

def render(state):
    st.caption("This is a controlled scheduling model. It does not create, suspend, or alter real operating-system processes.")
    with st.form("add_process"):
        a,b,c,d,e=st.columns(5); pid=a.text_input("PID",key="proc_pid"); name=b.text_input("Name",key="proc_name"); arrival=c.number_input("Arrival",0,100,0,key="proc_arr"); burst=d.number_input("Burst",1,100,3,key="proc_burst"); priority=e.number_input("Priority",0,20,1,key="proc_priority")
        if st.form_submit_button("Add simulated process"):
            if not pid or not name: st.error("PID and process name are required.")
            elif any(str(p["pid"])==pid for p in state["processes"]): st.error("Duplicate process ID.")
            else: state["processes"].append({"pid":pid,"name":name,"arrival":int(arrival),"burst":int(burst),"priority":int(priority)}); st.rerun()
    if st.button("Load demonstration workload",key="proc_demo"): state["processes"]=[{"pid":"P1","name":"Compiler","arrival":0,"burst":7,"priority":2},{"pid":"P2","name":"Browser","arrival":2,"burst":4,"priority":1},{"pid":"P3","name":"Editor","arrival":4,"burst":1,"priority":3},{"pid":"P4","name":"Backup","arrival":5,"burst":4,"priority":2}]; st.rerun()
    st.dataframe(pd.DataFrame(state["processes"]),use_container_width=True,hide_index=True)
    algo=st.selectbox("Scheduling algorithm",["FCFS","SJF (Non-preemptive)","Priority","Round Robin","SRTF"],key="sched_algo"); quantum=st.number_input("Round Robin quantum",1,20,2,key="sched_quantum")
    if st.button("Execute scheduling",key="sched_run"):
        try: state["schedule_result"]=schedule(state["processes"],algo,int(quantum))
        except ValueError as e: st.error(str(e))
    r=state.get("schedule_result")
    if r and r["rows"]:
        m=r["metrics"]; metrics([("CPU utilization",f"{m['cpu_utilization']:.1f}%","busy / elapsed"),("Average waiting",f"{m['avg_waiting']:.2f}","time units"),("Average turnaround",f"{m['avg_turnaround']:.2f}","time units"),("Throughput",f"{m['throughput']:.2f}","processes/time")]); st.dataframe(pd.DataFrame(r["rows"]),use_container_width=True,hide_index=True)
        g=pd.DataFrame(r["gantt"]); fig=px.timeline(g,x_start="start",x_end="end",y="pid",color="name",text="name",template="plotly_dark",title="Gantt chart"); fig.update_yaxes(autorange="reversed"); st.plotly_chart(fig,use_container_width=True)
