import Core

initP_Children = Core.ini()  # 创建初始进程
print("Tips: input help to show the command list \n")

while 1:
    command = input("Input command:")
    if command == "help":
        print(" create: create a process\n",
              "destroy: destroy a process\n",
              "request: request resources\n",
              "release: release resources\n",
              "time out: time out and schedule\n",
              "print pcb: show the information of pcb\n",
              "print ready list: show the information of ready list\n",
              "print block list: show the information of block list\n",
              "print resources: show the information of resources\n",
              "sd: close the shell and exit"
              )

    elif command == "sd":
        break

    elif command == "create":
        pid = input("Input PID:")
        status = input("Input Status:")
        priority = input("Input Priority:")
        Core.create_process(pid, status, priority)

    elif command == "destroy":
        pid = input("Input PID:")
        Core.destroy_process(pid)

    elif command == "request":
        rid = input("Input RID:")
        n = input("Input N:")
        Core.request_resource(rid, n)

    elif command == "release":
        rid = input("Input RID:")
        n = input("Input N:")
        Core.release_resource(rid, n)

    elif command == "time out":
        Core.time_out()

    elif command == "print pcb":
        pid = input("Input PID:")
        Core.print_pcb(pid)

    elif command == "print ready list":
        Core.print_ready_list()

    elif command == "print block list":
        Core.print_block_list()

    elif command == "print resources":
        Core.print_resources()

    else:
        print("Unknown command")

print("Exit")
