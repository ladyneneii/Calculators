from CPU_Processes import Process\

def RoundRobin(pInfo):
    while pInfo.plist or pInfo.queue:
        if pInfo.multi_feedback_check and (pInfo.plist and not pInfo.queue):
            return
        if not pInfo.multi_feedback_check:
            if pInfo.plist:
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
            if pInfo.queue[0][2] > 0:
                pInfo.queue.append(pInfo.queue[0])
            pInfo.queue.pop(0)
        if pInfo.queue:
            pInfo.orderOfProcesses.append(pInfo.queue[0][0])
            if pInfo.queue[0][2] > pInfo.QT:
                pInfo.queue[0][2] -= pInfo.QT
                pInfo.time += pInfo.QT
                if pInfo.multi_feedback_check:
                    pInfo.queue.append(pInfo.queue[0])
            else:
                pInfo.time += pInfo.queue[0][2]
                pInfo.queue[0][2] = 0
                integer_part = ''.join(char for char in pInfo.queue[0][0] if char.isdigit())
                pInfo.processes_list[int(integer_part) - 1].append(pInfo.time)
            pInfo.timestamps.append(pInfo.time)
            if pInfo.multi_feedback_check:
                for j in range(pInfo.mlfq_levels):
                    if j == pInfo.mlfq_levels - 1:
                        pInfo.mlfq_orderOfProcesses[j].append(pInfo.queue[0][0])
                    else:
                        pInfo.mlfq_orderOfProcesses[j].append(" ")
                    pInfo.mlfq_timestamps[j].append(pInfo.time)
                pInfo.queue.pop(0)
    if not pInfo.multi_feedback_check:
        pInfo.displayGanttChart()
        pInfo.calculateTable()
        pInfo.displayTable()
        pInfo.displayEfficiency()


if __name__ == "__main__":
    pInfo = Process("Round-Robin")
    pInfo.QT = 3 # SET THE QUANTUM TIME HERE
    # Customization
    # pInfo.processes_list = [
    #     ["P1", 10, 5, 3],
    #     ["P2", 1, 4, 1],
    #     ["P3", 12, 12, 6],
    #     ["P4", 3, 3, 7],
    #     ["P5", 2, 4, 2]
    # ]
    pInfo.multi_check = pInfo.prio_check = False
    pInfo.trimProcessList()

    RoundRobin(pInfo)



