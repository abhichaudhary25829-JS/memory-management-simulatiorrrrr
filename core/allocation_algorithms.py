"""Deterministic fixed-block allocation algorithms."""
from time import perf_counter

def run_allocation(block_sizes, processes, algorithm="First Fit"):
    """Processes are dicts: pid, name, size. Returns a complete calculated trial."""
    blocks=[{"id":i+1,"start":sum(block_sizes[:i]),"size":int(s),"remaining":int(s)} for i,s in enumerate(block_sizes)]
    cursor=0; results=[]; started=perf_counter()
    for p in processes:
        candidates=[b for b in blocks if b["remaining"] >= p["size"]]
        selected=None
        if candidates:
            if algorithm=="First Fit": selected=candidates[0]; why="first block that can satisfy the request"
            elif algorithm=="Best Fit": selected=min(candidates,key=lambda b:b["remaining"]); why="smallest sufficient remaining block"
            elif algorithm=="Worst Fit": selected=max(candidates,key=lambda b:b["remaining"]); why="largest sufficient remaining block"
            elif algorithm=="Next Fit":
                for offset in range(len(blocks)):
                    candidate=blocks[(cursor+offset)%len(blocks)]
                    if candidate["remaining"] >= p["size"]: selected=candidate; cursor=(candidate["id"])%len(blocks); break
                why="first sufficient block searched from the previous placement"
        if selected:
            before=selected["remaining"]; selected["remaining"]-=p["size"]
            start_address = selected["start"] + (selected["size"] - before)
            results.append({**p,"status":"Allocated","block":selected["id"],"start":start_address,"end":start_address+p["size"]-1,"internal_fragmentation":0,"explanation":f"Block {selected['id']} selected: {why}."})
        else: results.append({**p,"status":"Failed","block":None,"start":None,"end":None,"internal_fragmentation":0,"explanation":"No block has enough remaining contiguous capacity."})
    remaining=sum(b["remaining"] for b in blocks); largest=max((b["remaining"] for b in blocks),default=0)
    return {"algorithm":algorithm,"results":results,"blocks":blocks,"successful":sum(r["status"]=="Allocated" for r in results),"failed":sum(r["status"]=="Failed" for r in results),"remaining":remaining,"external_fragmentation":remaining-largest,"execution_time_ms":(perf_counter()-started)*1000}

def compare_algorithms(block_sizes, processes): return [run_allocation(block_sizes,processes,a) for a in ["First Fit","Best Fit","Worst Fit","Next Fit"]]
