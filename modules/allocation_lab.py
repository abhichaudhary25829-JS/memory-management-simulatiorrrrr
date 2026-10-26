import streamlit as st
import pandas as pd
from core.allocation_algorithms import run_allocation, compare_algorithms
from components.charts import bar

def _parse_ints(text): return [int(x.strip()) for x in text.split(',') if x.strip()]
def render(state):
    st.caption("Fixed-block allocation experiment. Each trial starts from the same supplied blocks; this makes comparisons deterministic.")
    blocks=st.text_input("Available block sizes (KB)","100, 500, 200, 300, 600",key="alloc_blocks")
    raw=st.text_area("Processes: one per line as PID, Name, Size", "P1, Compiler, 212\nP2, Browser, 417\nP3, Editor, 112\nP4, VM, 426",key="alloc_processes")
    algorithm=st.selectbox("Algorithm",["First Fit","Best Fit","Worst Fit","Next Fit"],key="alloc_algo")
    def parse(): return [{"pid":p[0].strip(),"name":p[1].strip(),"size":int(p[2].strip())} for line in raw.splitlines() if line.strip() for p in [line.split(',',2)]]
    c1,c2=st.columns(2)
    if c1.button("Run selected algorithm",key="alloc_run"):
        try: state["allocation_result"]=run_allocation(_parse_ints(blocks),parse(),algorithm); state["allocation_success"]=state["allocation_result"]["successful"]/len(parse())*100
        except (ValueError,IndexError) as e: st.error("Use positive comma-separated sizes and PID, Name, Size rows.")
    if c2.button("Compare all algorithms",key="alloc_compare"):
        try: state["allocation_comparison"]=compare_algorithms(_parse_ints(blocks),parse())
        except (ValueError,IndexError): st.error("Please correct the input data.")
    result=state.get("allocation_result")
    if result:
        st.subheader(f"{result['algorithm']} result"); st.dataframe(pd.DataFrame(result["results"]),use_container_width=True,hide_index=True)
        st.caption(f"Success: {result['successful']} · Failures: {result['failed']} · Remaining: {result['remaining']} KB · External fragmentation: {result['external_fragmentation']} KB · Measured execution: {result['execution_time_ms']:.4f} ms")
    comp=state.get("allocation_comparison")
    if comp:
        table=pd.DataFrame([{k:r[k] for k in ["algorithm","successful","failed","remaining","external_fragmentation","execution_time_ms"]} for r in comp]); st.subheader("Algorithm comparison"); st.dataframe(table,use_container_width=True,hide_index=True); st.plotly_chart(bar(table,"algorithm","successful","Successful allocations"),use_container_width=True)
