"""Safe, read-only psutil collection with portable fallbacks."""
from datetime import datetime
import psutil

def _safe(call, default=None):
    try: return call()
    except (psutil.Error, OSError, PermissionError): return default

def bytes_to_mb(value): return round((value or 0)/1024/1024, 2)

def snapshot():
    vm=psutil.virtual_memory(); swap=psutil.swap_memory(); disk_io=_safe(psutil.disk_io_counters); net=_safe(psutil.net_io_counters)
    freq=_safe(psutil.cpu_freq); root=_safe(lambda: psutil.disk_usage("C:\\") if __import__('platform').system()=="Windows" else psutil.disk_usage("/"))
    return {"timestamp":datetime.now().isoformat(timespec="seconds"),"cpu":psutil.cpu_percent(interval=0.1),"per_cpu":psutil.cpu_percent(interval=None,percpu=True),"frequency_mhz":round(freq.current,1) if freq else None,"logical_cores":psutil.cpu_count(True),"physical_cores":psutil.cpu_count(False),"ram_total_mb":bytes_to_mb(vm.total),"ram_used_mb":bytes_to_mb(vm.used),"ram_available_mb":bytes_to_mb(vm.available),"ram_percent":vm.percent,"swap_used_mb":bytes_to_mb(swap.used),"swap_percent":swap.percent,"disk_percent":root.percent if root else None,"disk_read_mb":bytes_to_mb(disk_io.read_bytes) if disk_io else None,"disk_write_mb":bytes_to_mb(disk_io.write_bytes) if disk_io else None,"net_sent_mb":bytes_to_mb(net.bytes_sent) if net else None,"net_recv_mb":bytes_to_mb(net.bytes_recv) if net else None,"process_count":len(psutil.pids())}

def partitions():
    rows=[]
    for p in _safe(psutil.disk_partitions,[]) or []:
        usage=_safe(lambda:psutil.disk_usage(p.mountpoint))
        if usage: rows.append({"Device":p.device,"Mount":p.mountpoint,"File system":p.fstype,"Used GB":round(usage.used/2**30,2),"Total GB":round(usage.total/2**30,2),"Usage %":usage.percent})
    return rows

def top_processes(sort="cpu", limit=12):
    rows=[]
    for proc in psutil.process_iter(["pid","name","status","cpu_percent","memory_percent","create_time"]):
        try:
            info=proc.info; created=datetime.fromtimestamp(info["create_time"]).strftime("%Y-%m-%d %H:%M") if info.get("create_time") else "Unavailable"
            rows.append({"PID":info["pid"],"Name":info.get("name") or "Unknown","Status":info.get("status") or "Unknown","CPU %":round(info.get("cpu_percent") or 0,2),"Memory %":round(info.get("memory_percent") or 0,2),"Created":created})
        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess): pass
    key="CPU %" if sort=="cpu" else "Memory %"; return sorted(rows,key=lambda r:r[key],reverse=True)[:limit]
