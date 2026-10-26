from core.memory_manager import MemoryManager
from core.allocation_algorithms import run_allocation
from core.paging_engine import simulate_replacement, translate_address
from core.process_scheduler import schedule
from core.disk_scheduler import disk_schedule

def test_memory_compaction():
    m=MemoryManager(100); assert m.allocate("1","A",40)[0]; assert m.allocate("2","B",30)[0]; m.deallocate("1"); assert m.external_fragmentation==30; m.compact(); assert m.external_fragmentation==0
def test_allocation():
    result=run_allocation([100],[{"pid":"P1","name":"P1","size":50},{"pid":"P2","name":"P2","size":25}])
    assert result["successful"]==2
    assert [row["start"] for row in result["results"]]==[0,50]
def test_paging_and_translation():
    assert simulate_replacement([1,2,1],2,"FIFO")["hits"]==1; assert translate_address(65,64,256,{1:2})["physical_address"]==129
def test_scheduling(): assert schedule([{"pid":"P","name":"P","arrival":0,"burst":3,"priority":1}])["rows"][0]["Waiting"]==0
def test_disk(): assert disk_schedule([20,10],0,100,"FCFS")["movement"]==30
