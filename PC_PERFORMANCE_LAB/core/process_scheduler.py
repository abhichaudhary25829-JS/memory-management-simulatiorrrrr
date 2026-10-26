from dataclasses import dataclass, asdict

def schedule(processes, algorithm="FCFS", quantum=2):
    if not processes: return {"rows":[],"gantt":[],"metrics":{}}
    ps=[dict(p, remaining=int(p["burst"])) for p in processes]
    for p in ps:
        if p["arrival"]<0 or p["burst"]<=0: raise ValueError("Arrival must be >= 0 and burst must be positive")
        p.setdefault("priority",0); p["start"]=None; p["response"]=None
    time=0; completed=[]; gantt=[]; ready=[]; arrivals=sorted(ps,key=lambda p:p["arrival"])
    def admit():
        nonlocal arrivals
        ready.extend([p for p in arrivals if p["arrival"]<=time]); arrivals=[p for p in arrivals if p["arrival"]>time]
    while len(completed)<len(ps):
        admit()
        if not ready:
            time=arrivals[0]["arrival"]; admit()
        if algorithm=="FCFS": current=ready.pop(0); run=current["remaining"]
        elif algorithm=="SJF (Non-preemptive)": current=min(ready,key=lambda p:p["burst"]); ready.remove(current); run=current["remaining"]
        elif algorithm=="Priority": current=min(ready,key=lambda p:(p["priority"],p["arrival"])); ready.remove(current); run=current["remaining"]
        elif algorithm=="SRTF": current=min(ready,key=lambda p:p["remaining"]); ready.remove(current); run=1
        else: current=ready.pop(0); run=min(quantum,current["remaining"])
        start=time
        if current["start"] is None: current["start"]=time; current["response"]=time-current["arrival"]
        time+=run; current["remaining"]-=run; gantt.append({"pid":current["pid"],"name":current["name"],"start":start,"end":time,"duration":run})
        admit()
        if current["remaining"]>0: ready.append(current)
        else: current["completion"]=time; completed.append(current)
    rows=[]
    for p in sorted(ps,key=lambda x:str(x["pid"])):
        turnaround=p["completion"]-p["arrival"]; waiting=turnaround-p["burst"]
        rows.append({"PID":p["pid"],"Name":p["name"],"Arrival":p["arrival"],"Burst":p["burst"],"Priority":p["priority"],"Completion":p["completion"],"Turnaround":turnaround,"Waiting":waiting,"Response":p["response"]})
    busy=sum(p["burst"] for p in ps); span=max(p["completion"] for p in ps)-min(p["arrival"] for p in ps)
    return {"rows":rows,"gantt":gantt,"metrics":{"cpu_utilization":busy/span*100 if span else 0,"throughput":len(ps)/span if span else 0,"avg_waiting":sum(r["Waiting"] for r in rows)/len(rows),"avg_turnaround":sum(r["Turnaround"] for r in rows)/len(rows),"avg_response":sum(r["Response"] for r in rows)/len(rows)}}
