def simulate_replacement(reference, frame_count, algorithm="FIFO", step_limit=None):
    if frame_count <= 0: raise ValueError("Frame count must be positive")
    frames=[]; faults=hits=0; steps=[]; fifo_index=0; last_used={}
    seq=reference[:step_limit] if step_limit else reference
    for i,page in enumerate(seq):
        evicted=None; hit=page in frames
        if hit: hits+=1
        else:
            faults+=1
            if len(frames)<frame_count: frames.append(page)
            else:
                if algorithm=="FIFO": victim=fifo_index; fifo_index=(fifo_index+1)%frame_count
                elif algorithm=="LRU": victim=min(range(frame_count),key=lambda x:last_used.get(frames[x],-1))
                else: # Optimal: farthest future use (or never used again)
                    future=seq[i+1:]; victim=max(range(frame_count),key=lambda x: future.index(frames[x]) if frames[x] in future else float("inf"))
                evicted=frames[victim]; frames[victim]=page
        last_used[page]=i
        steps.append({"step":i+1,"page":page,"result":"Hit" if hit else "Fault","evicted":evicted,"frames":" | ".join(map(str,frames))})
    total=len(seq)
    return {"algorithm":algorithm,"steps":steps,"frames":frames,"hits":hits,"faults":faults,"hit_ratio":hits/total if total else 0,"fault_ratio":faults/total if total else 0}

def translate_address(logical_address, page_size, logical_size, page_table):
    if logical_address < 0 or logical_address >= logical_size: return {"valid":False,"message":"Invalid logical address: outside logical address space."}
    page=logical_address//page_size; offset=logical_address%page_size
    if page not in page_table: return {"valid":False,"page":page,"offset":offset,"message":"Page fault: the page is not mapped to a frame."}
    frame=page_table[page]; return {"valid":True,"page":page,"offset":offset,"frame":frame,"physical_address":frame*page_size+offset}
