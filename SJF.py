from CPU_Processes import Process

def SJF(pInfo):
    while pInfo.plist or pInfo.queue:
        if pInfo.multi_feedback_check and (pInfo.plist and not pInfo.queue):
            return
        if not pInfo.multi_check and not pInfo.multi_feedback_check and pInfo.plist:
            if not pInfo.queue and pInfo.plist[0][1] > pInfo.time:
                pInfo.time = pInfo.plist[0][1]
                pInfo.timestamps.append(pInfo.time)
                pInfo.orderOfProcesses.append('idle')
            while True:
                if pInfo.plist and pInfo.plist[0][1] <= pInfo.time:
                    pInfo.queue.append(pInfo.plist[0])
                    pInfo.plist.pop(0)
                else:
                    break
        if not pInfo.multi_check:
            pInfo.min_process = min(pInfo.queue, key=lambda x: (x[2], x[1], x[0]))
        pInfo.time += pInfo.min_process[2]
        pInfo.timestamps.append(pInfo.time)
        pInfo.orderOfProcesses.append(pInfo.min_process[0])
        integer_part = ''.join(char for char in pInfo.min_process[0] if char.isdigit())
        pInfo.processes_list[int(integer_part) - 1].append(pInfo.time)
        pInfo.queue.remove(pInfo.min_process)
        if pInfo.multi_feedback_check:
            for j in range(pInfo.mlfq_levels):
                if j == pInfo.mlfq_levels - 1:
                    pInfo.mlfq_orderOfProcesses[j].append(pInfo.min_process[0])
                else:
                    pInfo.mlfq_orderOfProcesses[j].append(" ")
                pInfo.mlfq_timestamps[j].append(pInfo.time)
        if pInfo.multi_check:
            print("MULTILEVEL QUEUE CHECK: SJF")
            return
    if not pInfo.multi_feedback_check:
        pInfo.displayGanttChart()
        pInfo.calculateTable()
        pInfo.displayTable()
        pInfo.displayEfficiency()


if __name__ == "__main__":
    pInfo = Process("SJF")
    # Customization
    # pInfo.processes_list = [
    #     ["P1", 10, 5],
    #     ["P2", 1, 4],
    #     ["P3", 12, 12],
    #     ["P4", 3, 3],
    #     ["P5", 2, 5]
    # ]
    # algo3 already has values by default, making multi_check True, leading to errors because if multi_check is True,
    # the program will not run line 16, so set it to False if you are not running an MLQ algorithm.
    pInfo.multi_check = pInfo.prio_check = False
    pInfo.trimProcessList()

    SJF(pInfo)



