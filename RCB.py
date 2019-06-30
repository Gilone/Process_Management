class RcBBlock:
    def __init__(self, rid=None, resources=None, waiting_lists=None):
        self._RID = rid   # 资源号
        self._ResourcesOverall = resources  # 资源总数
        self._ResourcesUseful = resources   # 资源可用单元
        self._WaitingLists = waiting_lists   # 阻塞队列

    def print_rid(self):
        print("RID:", self._RID, "|", "ResourcesOverall:", self._ResourcesOverall, "|",
              "ResourcesUseful:",  self._ResourcesUseful)

    def get_rid(self):
        return self._RID

    def get_resources_overall(self):
        return self._ResourcesOverall

    def get_resources_useful(self):
        return self._ResourcesUseful

    def get_waiting_list(self):
        return self._WaitingLists

    def set_resources_useful(self, r):
        self._ResourcesUseful = r

    def set_waiting_list(self, r):
        self._WaitingLists = r


class WaitingBlock:
    def __init__(self, p_block=None, req_num=None, next_block=None):
        self._PBlock = p_block    # 阻塞的PCB
        self._Req_Num = req_num   # 阻塞的PCB所请求的资源数
        self._NextBlock = next_block

    def get_p_block(self):
        return self._PBlock

    def get_req_num(self):
        return self._Req_Num

    def get_next_block(self):
        return self._NextBlock

    def set_p_block(self, r):
        self._PBlock = r

    def set_req_num(self, r):
        self._Req_Num = r

    def set_next_block(self, r):
        self._NextBlock = r


class WaitingLists:
    def __init__(self):      # 初始化链表为空表
        self._head = None
        self._tail = None

    def get_head(self):
        return self._head

    def is_empty(self):  # 检测是否为空
        return self._head is None

    def append_list_last(self, value, req_num):  # 在链表尾部添加元素
        new_node = WaitingBlock(value, req_num)
        if self.is_empty():
            self._head = new_node  # 若为空表，将添加的元素设为第一个元素
        else:
            current = self._head
            while current.get_next_block() is not None:
                current = current.get_next_block()  # 遍历链表
            current.set_next_block(new_node)  # 此时current为链表最后的元素

    def append_list_first(self, value, req_num):  # 在链表首部添加元素
        new_node = WaitingBlock(value, req_num)
        if self.is_empty():
            self._head = new_node  # 若为空表，将添加的元素设为第一个元素
        else:
            current = self._head
            self._head = new_node
            self._head.set_next_block(current)

    def append_list_first_to_last(self):  # 从链首扔到链尾
        node = self._head
        current = self._head
        if current.get_next_block() is not None:
            self._head = current.get_next_block()
            while current.get_next_block() is not None:
                current = current.get_next_block()  # 遍历链表
            current.set_next_block(node)  # 此时current为链表最后的元素

    def remove(self, value):  # remove删除链表中的某项元素
        current = self._head
        pre = None
        while current is not None:
            if current.get_p_block().get_pid() == value:
                if not pre:
                    self._head = current.get_next_block()
                else:
                    pre.set_next_block(current.get_next_block())
                break
            else:
                pre = current
                current = current.get_next_block()

    def search(self, value):  # search检索元素是否在链表中
        current = self._head
        found_value = False
        while current is not None and not found_value:
            if current.get_p_block().get_pid() == value:
                found_value = True
            else:
                current = current.get_next_block()
        if found_value:
            return current.get_p_block()
        return None

    def print_all(self):
        current = self._head
        while current is not None:
            print("Process：")
            current.get_p_block().print_pcb()
            current = current.get_next_block()
