import PCB
import RCB
import ReadyList

ready_list = [ReadyList.ReadyLists(), ReadyList.ReadyLists(), ReadyList.ReadyLists()]
rcb_list = [RCB.RcBBlock('1', 1, RCB.WaitingLists()), RCB.RcBBlock('2', 2, RCB.WaitingLists()),
            RCB.RcBBlock('3', 3, RCB.WaitingLists()), RCB.RcBBlock('4', 4, RCB.WaitingLists())]


def find_pcb(pid):   # 根据PID找到对应的进程控制块
    for i in range(3):
        if ready_list[i].search(pid) is not None:
            return ready_list[i].search(pid), i
    for i in range(4):
        if rcb_list[i].get_waiting_list().search(pid) is not None:
            return rcb_list[i].get_waiting_list().search(pid), i+3
    return None, None


def remove_from_list(pid):   # 把一个进程从所有队列中删除
    for i in range(3):
        ready_list[i].remove(pid)
    for i in range(4):
        rcb_list[i].get_waiting_list().remove(pid)


def find_top_priority():   # 找到当前队列中优先级最高，最开始的进程控制块
    if ready_list[2].get_head() is not None:
        return ready_list[2].get_head().get_pcb_block()
    elif ready_list[1].get_head() is not None:
        return ready_list[1].get_head().get_pcb_block()
    else:
        return ready_list[0].get_head().get_pcb_block()


def ini():   # 初始化
    global running_p
    init_p = PCB.PcBBlock("Initial P", "Running", 0, PCB.ChildrenList())
    ready_list[0].append_list_last(init_p)
    running_p = init_p
    return init_p   # 创建一个初始进程块


def create_process(pid, status, priority):   # 创建一个进程
    global running_p
    new_pcb = PCB.PcBBlock(pid, status, priority, PCB.ChildrenList())  # 建立新的进程块
    parent = running_p
    new_pcb.set_parent(parent)
    parent.get_children_list().append_list(new_pcb)  # 加入父进程的子进程链表
    ready_list[int(priority)].append_list_last(new_pcb)   # 加入ready链表尾
    print("Successfully create \n")
    # scheduler()


def destroy_process(pid):
    pcb, cat = find_pcb(pid)
    if pcb is None:
        print("Did not find this pid")
        return
    for i in range(4):
        release_resource(i, pcb.get_resources[i])  # 把资源释放了再销毁进程
    if not pcb.get_children_list().is_empty():
        destroy_process(pcb.get_children_list().get_head().get_pcb_block().get_pid())
    pcb.get_parent().get_children_list().remove(pid)  # 从父进程的子进程链表中删除
    remove_from_list(pid)
    del pcb
    print("Successfully destroy \n")
    scheduler()


def request_resource(rid, n):
    rid = str(rid)
    n = int(n)
    global running_p
    process = running_p
    if rid != '1' and rid != '2' and rid != '3' and rid != '4':
        print("No such RID")
        return
    if rcb_list[int(rid)-1].get_resources_useful() >= n:    # 可以分配资源
        rcb_list[int(rid)-1].set_resources_useful(rcb_list[int(rid)-1].get_resources_useful()-n)
        process.set_resources(rid, process.get_resources(rid)+n)
        print("Successfully allocate \n")
    else:
        if rcb_list[int(rid)-1].get_resources_overall() < n:   # 资源申请超过总数
            print("Request too much \n")
            return
        process.set_status("Blocked")
        ready_list[int(process.get_priority())].remove(process.get_pid())   # 移除就绪列表
        rcb_list[int(rid)-1].get_waiting_list().append_list_last(process, n)  # 移入阻塞列表
        print("Resources exhausted,and process has been blocked \n")
    scheduler()


def release_resource(rid, n):
    rid = str(rid)
    n = int(n)
    global running_p
    process = running_p
    if rid != '1' and rid != '2' and rid != '3' and rid != '4':
        print("No such RID")
        return
    rcb_list[int(rid)-1].set_resources_useful(rcb_list[int(rid)-1].get_resources_useful()+n)  # 释放资源
    process.set_resources(rid, process.get_resources(rid)-n)
    while rcb_list[int(rid)-1].get_waiting_list().get_head() is not None:   # 阻塞队列不为空
        if rcb_list[int(rid)-1].get_waiting_list().get_head().get_req_num() <= \
                rcb_list[int(rid)-1].get_resources_useful():   # 阻塞队列中的请求得到满足
            req_num = rcb_list[int(rid)-1].get_waiting_list().get_head().get_req_num()
            rcb_list[int(rid)-1].set_resources_useful(rcb_list[int(rid)-1].get_resources_useful() -
                                                      req_num)
            process = rcb_list[int(rid)-1].get_waiting_list().get_head().get_p_block()
            rcb_list[int(rid)-1].get_waiting_list().remove(process.get_pid())
            process.set_status("Ready")
            process.set_resources(rid, process.get_resources(rid) + req_num)  # 分配资源
            ready_list[int(process.get_priority())].append_list_last(process)
    print("Successfully release \n")
    scheduler()


def scheduler():  # 调度，让优先级最高的运行
    global running_p
    process = find_top_priority()
    running_p = process
    process.set_status("Running")


def time_out():    # 时间片超时
    global running_p
    # process = find_running()
    # process.set_status("Ready")
    running_p.set_status("Ready")
    ready_list[int(running_p.get_priority())].append_list_first_to_last()
    print("Successfully schedule \n")
    scheduler()


def print_ready_list():
    for i in range(3):
        print("Priority:", i)
        ready_list[i].print_all()
    print("\n")


def print_block_list():
    for i in range(4):
        print("Resource Number", i+1, ":")
        rcb_list[i].get_waiting_list().print_all()
    print("\n")


def print_resources():
    for i in range(4):
        print("Resource Number", i+1, ":")
        rcb_list[i].print_rid()
    print("\n")


def print_pcb(pid):
    pcb, cat = find_pcb(pid)
    if pcb is None:
        print("Did not find this pid")
        return
    pcb.print_pcb()
    print("\n")
