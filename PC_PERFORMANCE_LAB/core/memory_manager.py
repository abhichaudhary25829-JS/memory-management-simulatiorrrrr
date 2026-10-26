"""Contiguous memory allocation model used by the memory laboratory."""
from dataclasses import dataclass, asdict

@dataclass
class Block:
    block_id: int
    start: int
    size: int
    process_id: str | None = None
    process_name: str | None = None
    requested: int = 0
    reserved: bool = False
    @property
    def end(self): return self.start + self.size - 1
    @property
    def free(self): return self.process_id is None and not self.reserved
    @property
    def internal_frag(self): return max(0, self.size - self.requested) if self.process_id else 0
    def to_dict(self):
        d = asdict(self); d.update({"end": self.end, "status": "Reserved" if self.reserved else "Free" if self.free else "Allocated", "internal_fragmentation": self.internal_frag})
        return d

class MemoryManager:
    def __init__(self, total=1024, partitions=None):
        if total <= 0: raise ValueError("Total memory must be positive")
        self.total = total
        self.blocks = []
        start = 0
        for size in partitions or [total]:
            if size <= 0 or start + size > total: raise ValueError("Invalid partition layout")
            self.blocks.append(Block(len(self.blocks)+1, start, size)); start += size
        if start < total: self.blocks.append(Block(len(self.blocks)+1, start, total-start))
        self.events = []
    def _event(self, text): self.events.append({"event": text, "used": self.used, "free": self.free})
    @property
    def used(self): return sum(b.size for b in self.blocks if b.process_id)
    @property
    def free(self): return sum(b.size for b in self.blocks if b.free)
    @property
    def internal_fragmentation(self): return sum(b.internal_frag for b in self.blocks)
    @property
    def external_fragmentation(self):
        free = [b.size for b in self.blocks if b.free]
        return sum(free) - max(free, default=0)
    def allocate(self, pid, name, requested, strategy="First Fit"):
        if not str(pid).strip() or not name.strip() or requested <= 0: raise ValueError("Process ID, name, and positive memory size are required")
        if requested > self.total: raise ValueError("Request exceeds total simulated memory")
        if any(b.process_id == str(pid) for b in self.blocks): raise ValueError("Duplicate process ID")
        candidates = [b for b in self.blocks if b.free and b.size >= requested]
        if not candidates:
            reason = "No contiguous block is large enough" if self.free >= requested else "Insufficient total free memory"
            self._event(f"Allocation failed for {pid}: {reason}"); return False, reason
        if strategy == "Best Fit": target = min(candidates, key=lambda b:b.size)
        elif strategy == "Worst Fit": target = max(candidates, key=lambda b:b.size)
        else: target = candidates[0]
        # Split dynamic partition: allocation consumes exactly the request, so internal fragmentation is zero.
        index = self.blocks.index(target)
        allocated = Block(target.block_id, target.start, requested, str(pid), name, requested)
        replacement = [allocated]
        if target.size > requested: replacement.append(Block(0, target.start+requested, target.size-requested))
        self.blocks[index:index+1] = replacement
        self._renumber(); self._event(f"Allocated {requested} KB to {name} ({pid}) using {strategy}")
        return True, allocated
    def deallocate(self, pid):
        found = [b for b in self.blocks if b.process_id == str(pid)]
        if not found: raise ValueError("Process does not exist in allocated memory")
        for b in found: b.process_id = b.process_name = None; b.requested = 0
        self._merge(); self._event(f"Released memory for process {pid}")
    def _merge(self):
        merged=[]
        for b in self.blocks:
            if merged and b.free and merged[-1].free and merged[-1].end+1 == b.start: merged[-1].size += b.size
            else: merged.append(b)
        self.blocks=merged; self._renumber()
    def _renumber(self):
        for i,b in enumerate(self.blocks,1): b.block_id=i
    def compact(self):
        cursor=0; allocated=[]
        for b in self.blocks:
            if b.process_id:
                b.start=cursor; cursor+=b.size; allocated.append(b)
        if cursor < self.total: allocated.append(Block(len(allocated)+1,cursor,self.total-cursor))
        self.blocks=allocated; self._renumber(); self._event("Memory compacted; all free space merged")
    def snapshot(self):
        return {"total":self.total,"blocks":[b.to_dict() for b in self.blocks],"used":self.used,"free":self.free,"internal_fragmentation":self.internal_fragmentation,"external_fragmentation":self.external_fragmentation,"utilization":self.used/self.total*100,"events":self.events}
