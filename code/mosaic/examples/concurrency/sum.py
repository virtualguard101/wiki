def T_worker():
    t = heap.x
    sys_sched()
    heap.x = t + 1
    sys_sched()

def main():
    heap.x = 0
    sys_spawn(T_worker)
    sys_spawn(T_worker)

