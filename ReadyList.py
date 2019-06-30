class ReadyBlock:
    def __init__(self, pcb_block=None, next_block=None):
        self._PCBBlock = pcb_block
        self._NextBlock = next_block

    def get_pcb_block(self):
        return self._PCBBlock

    def get_next_block(self):
        return self._NextBlock

    def set_pcb_block(self, new_value):
        self._PCBBlock = new_value

    def set_next_block(self, new_next):
        self._NextBlock = new_next


class ReadyLists:
    def __init__(self):      # 初始化链表为空表
        self._head = None
        self._tail = None

    def get_head(self):
        return self._head

    def is_empty(self):       # 检测是否为空
        return self._head is None

    def append_list_last(self, value):     # 在链表尾部添加元素
        new_node = ReadyBlock(value)
        if self.is_empty():
            self._head = new_node   # 若为空表，将添加的元素设为第一个元素
        else:
            current = self._head
            while current.get_next_block() is not None:
                current = current.get_next_block()   # 遍历链表
            current.set_next_block(new_node)   # 此时current为链表最后的元素

    def append_list_first(self, value):     # 在链表首部添加元素
        new_node = ReadyBlock(value)
        if self.is_empty():
            self._head = new_node   # 若为空表，将添加的元素设为第一个元素
        else:
            current = self._head
            self._head = new_node
            self._head.set_next_block(current)

    def append_list_first_to_last(self):     # 从链首扔到链尾
        origin_head = self._head
        if origin_head.get_next_block() is not None:
            self._head = origin_head.get_next_block()
            current = self._head
            while current.get_next_block() is not None:
                current = current.get_next_block()   # 遍历链表
            current.set_next_block(origin_head)   # 此时current为链表最后的元素
            origin_head.set_next_block(None)

    def remove(self, value):      # remove删除链表中的某项元素
        current = self._head
        pre = None
        while current is not None:
            if current.get_pcb_block().get_pid() == value:
                if not pre:
                    self._head = current.get_next_block()
                else:
                    pre.set_next_block(current.get_next_block())
                break
            else:
                pre = current
                current = current.get_next_block()

    def search(self, value):      # search检索元素是否在链表中
        current = self._head
        found_value = False
        while current is not None and not found_value:
            if current.get_pcb_block().get_pid() == value:
                found_value = True
            else:
                current = current.get_next_block()
        if found_value:
            return current.get_pcb_block()
        return None

    def print_all(self):
        current = self._head
        while current is not None:
            print("Process：")
            current.get_pcb_block().print_pcb()
            current = current.get_next_block()


