from CPU_Processes import Process
from FCFS import FCFS
from SJF import SJF
from PriorityNP import PriorityNP
from PriorityP import PriorityP
from RoundRobin import RoundRobin
from SRTF import SRTF
from MLQ import MLQ
from MLFQ import MLFQ

if __name__ == "__main__":
    pInfo = Process("FCFS")
    pInfo.multi_check = pInfo.prio_check = False
    pInfo.trimProcessList()
    print("FCFS:")
    FCFS(pInfo)

    pInfo2 = Process("SJF")
    pInfo2.multi_check = pInfo2.prio_check = False
    pInfo2.trimProcessList()
    print("\n\nSJF:")
    SJF(pInfo2)

    pInfo3 = Process("Priority-NP")
    pInfo3.multi_check = False
    pInfo3.trimProcessList()
    print("\n\nPriority (Non-Preemptive):")
    PriorityNP(pInfo3)

    pInfo4 = Process("Priority-P")
    pInfo4.multi_check = False
    pInfo4.trimProcessList()
    print("\n\nPriority (Preemptive):")
    PriorityP(pInfo4)

    pInfo5 = Process("Round-Robin")
    pInfo5.QT = 3
    pInfo5.multi_check = pInfo5.prio_check = False
    pInfo5.trimProcessList()
    print(f"\n\nRound Robin (Quantum Time: {pInfo5.QT}):")
    RoundRobin(pInfo5)

    pInfo6 = Process("SRTF")
    pInfo6.multi_check = pInfo6.prio_check = False
    pInfo6.trimProcessList()
    print("\n\nSRTF:")
    SRTF(pInfo6)

    pInfo7 = Process("MLQ", *("PriorityP", "SRTF", "FCFS"))
    # pInfo7 = Process("MLQ", *("PriorityNP", "SRTF"))
    pInfo7.trimProcessList()
    print(f"\n\nMLQ (Algorithms: {pInfo7.algorithms}):")
    MLQ(pInfo7)

    pInfo8 = Process("MLFQ", *("PriorityP", "SRTF", "FCFS"))
    # pInfo8 = Process("MLFQ", "SJF")
    pInfo8.QT = 2
    pInfo8.mlfq_levels = 5
    pInfo8.mlfq_qt = [2, 1, 2, 1]
    pInfo8.trimProcessList()
    print("\n\nMLFQ:")
    MLFQ(pInfo8)
