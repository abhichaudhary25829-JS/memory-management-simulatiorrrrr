import streamlit as st
import pandas as pd
from core.paging_engine import simulate_replacement, translate_address
from components.metric_cards import metrics

def render(state):
    logical=st.number_input("Logical address space (bytes)",64,65536,1024,key="pg_logical"); page_size=st.selectbox("Page size (bytes)",[16,32,64,128,256],index=2,key="pg_size"); physical=st.number_input("Physical memory (bytes)",page_size,65536,256,key="pg_physical")
    frames=max(1,int(physical)//int(page_size)); st.caption(f"Configuration: {logical//page_size} logical pages and {frames} physical frames.")
    refs=st.text_input("Page reference sequence", "7,0,1,2,0,3,0,4,2,3,0,3,2",key="pg_refs"); algo=st.selectbox("Replacement algorithm",["FIFO","LRU","Optimal"],key="pg_algo")
    a,b=st.columns(2)
    if a.button("Run full sequence",key="pg_run"):
        try: state["paging_result"]=simulate_replacement([int(x.strip()) for x in refs.split(',') if x.strip()],frames,algo)
        except ValueError: st.error("References must be comma-separated integer page numbers.")
    if b.button("Run one step",key="pg_step"):
        try:
            seq=[int(x.strip()) for x in refs.split(',') if x.strip()]; state["paging_step"]=min(state.get("paging_step",0)+1,len(seq)); state["paging_result"]=simulate_replacement(seq,frames,algo,state["paging_step"])
        except ValueError: st.error("Correct the reference sequence.")
    r=state.get("paging_result")
    if r:
        metrics([("Page faults",r["faults"],"required loads"),("Page hits",r["hits"],"already resident"),("Hit ratio",f"{r['hit_ratio']*100:.1f}%","hits / references"),("Fault ratio",f"{r['fault_ratio']*100:.1f}%","faults / references")]); st.dataframe(pd.DataFrame(r["steps"]),use_container_width=True,hide_index=True)
    st.subheader("Logical → physical address translation")
    address=st.number_input("Logical address",0,int(logical)+100,0,key="pg_address")
    if st.button("Translate address",key="pg_translate"):
        table={i:i%frames for i in range(int(logical)//int(page_size))}; out=translate_address(int(address),int(page_size),int(logical),table); st.success(f"Page {out['page']} → Frame {out['frame']}; offset {out['offset']}; physical address {out['physical_address']}") if out["valid"] else st.warning(out["message"])
    st.caption("Formulas: page number = logical address ÷ page size; offset = logical address mod page size; physical address = frame × page size + offset; hit/fault ratio = hits/faults ÷ total references.")
