def disk_schedule(requests, head, disk_size, algorithm="FCFS", direction="up"):
    if not all(0 <= x < disk_size for x in requests) or not 0 <= head < disk_size: raise ValueError("Requests and head must lie within disk cylinders")
    pending=list(requests); order=[]; current=head
    if algorithm=="FCFS": order=pending
    elif algorithm=="SSTF":
        while pending:
            nxt=min(pending,key=lambda x:(abs(x-current),x)); order.append(nxt); pending.remove(nxt); current=nxt
    else:
        lower=sorted([x for x in pending if x< head]); upper=sorted([x for x in pending if x>=head])
        if direction=="up":
            if algorithm=="SCAN": order=upper+[disk_size-1]+lower[::-1]
            elif algorithm=="C-SCAN": order=upper+[disk_size-1,0]+lower
            elif algorithm=="LOOK": order=upper+lower[::-1]
            else: order=upper+lower
        else:
            if algorithm=="SCAN": order=lower[::-1]+[0]+upper
            elif algorithm=="C-SCAN": order=lower[::-1]+[0,disk_size-1]+upper[::-1]
            elif algorithm=="LOOK": order=lower[::-1]+upper
            else: order=lower[::-1]+upper[::-1]
    path=[head]+order; distances=[abs(path[i]-path[i-1]) for i in range(1,len(path))]
    return {"algorithm":algorithm,"order":order,"path":path,"movement":sum(distances),"average_seek":sum(distances)/len(requests) if requests else 0,"distances":distances}
