class PcBBlock:
    def __init__(self, pid=None, status=None,  priority=None, children=None, parent=None
                 ):
        self._PID = pid    # 进程ID
        self._Resources = {'1': 0, '2': 0, '3': 0, '4': 0}  # 使用资源的状态，采用字典的数据结构，资源号作为KEY
        self._Status = status    # 资源的状态
        self._Parent_pcb = parent   # 父进程的进程控制块
        self._Children_list = children  # 子进程的链表
        self._Priority = priority    # 优先级

    def print_pcb(self):   # 打印PCB信息
        if self._Parent_pcb is None:
            parent_pid = None
        else:
            parent_pid = self._Parent_pcb.get_pid()
        print("PID:", self._PID, "|", "State:",  self._Status, "|",
              "Resources:", self._Resources, "|", "Parent:", parent_pid)

    def get_pid(self):   # 访问类内信息的方法
        return self._PID

    def get_children_list(self):
        return self._Children_list

    def get_parent(self):
        return self._Parent_pcb

    def get_priority(self):
        return self._Priority

    def get_resources(self, r):
        return self._Resources[r]

    def set_status(self, status):   # 更改类内信息的方法
        self._Status = status

    def set_resources(self, r, resources):
        self._Resources[r] = resources

    def set_parent(self, parent):
        self._Parent_pcb = parent

    def set_children(self, children):
        self._Children_list = children


class ChildrenBlock:    # 子进程链表的节点
    def __init__(self, pcb_block=None, brother=None):
        self._PCBBlock = pcb_block
        self._NextBrother = brother

    def get_pcb_block(self):
        return self._PCBBlock

    def get_next_brother(self):
        return self._NextBrother

    def set_pcb_block(self, new_value):
        self._PCBBlock = new_value

    def set_next_brother(self, new_next):
        self._NextBrother = new_next


class ChildrenList:    # 子进程链表
    def __init__(self):      # 初始化链表为空表
        self._head = None
        self._tail = None

    def is_empty(self):       # 检测是否为空
        return self._head is None

    def get_head(self):
        return self._head

    def append_list(self, value):     # 在链表尾部添加元素
        new_node = ChildrenBlock(value)
        if self.is_empty():
            self._head = new_node   # 若为空表，将添加的元素设为第一个元素
        else:
            current = self._head
            while current.get_next_brother() is not None:
                current = current.get_next_brother()   # 遍历链表
            current.set_next_brother(new_node)   # 此时current为链表最后的元素

    def search(self, value):      # search检索元素是否在链表中
        current = self._head
        found_value = False
        while current is not None and not found_value:
            if current.get_pcb_block().get_pid() == value:
                found_value = True
            else:
                current = current.get_next_brother()
        if found_value:
            return current.get_pcb_block()
        return None

    def remove(self, value):      # remove删除链表中的某项元素
        current = self._head
        pre = None
        while current is not None:
            if current.get_pcb_block().get_pid() == value:
                if not pre:
                    self._head = current.get_next_brother()
                else:
                    pre.set_next_brother(current.get_next_brother())
                break
            else:
                pre = current
                current = current.get_next_brother()
