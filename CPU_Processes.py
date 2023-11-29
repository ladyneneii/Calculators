import copy


class Process:
    # processes_list = [
    #     ["P1", 10, 5, 2],
    #     ["P2", 8, 4, 1],
    #     ["P3", 12, 4, 1],
    #     ["P4", 3, 3, 2],
    #     ["P5", 15, 5, 2]
    # ]

    # processes_list = [
    #     ["P1", 5, 30, 4],
    #     ["P2", 25, 15, 3],
    #     ["P3", 15, 25, 1],
    #     ["P4", 10, 10, 1],
    #     ["P5", 20, 35, 2],
    #     ["P6", 13, 5, 5]
    # ]

    # processes_list = [
    #     ["P1", 10, 5],
    #     ["P2", 8, 4],
    #     ["P3", 12, 4],
    #     ["P4", 3, 3],
    #     ["P5", 15, 5]
    # ]
    # 10 8 12 3 15
    # 5 4 4 3 5

    # processes_list = [
    #     ["P1", 10, 5, 2, 1],
    #     ["P2", 8, 4, 1, 2],
    #     ["P3", 12, 4, 1, 2],
    #     ["P4", 3, 3, 2, 1],
    #     ["P5", 15, 5, 2, 1]
    # ]

    # processes_list = [
    #     ["P1", 3, 6],
    #     ["P2", 8, 4],
    #     ["P3", 0, 7],
    #     ["P4", 12, 3],
    #     ["P5", 16, 5],
    #     ["P6", 5, 2],
    #     ["P7", 18, 7],
    #     ["P8", 10, 8],
    #     ["P9", 2, 1],
    #     ["P10", 14, 9]
    # ]

    # With Priority
    # processes_list = [
    #     ["P1", 3, 4, 2],
    #     ["P2", 5, 9, 1],
    #     ["P3", 8, 4, 2],
    #     ["P4", 0, 7, 1],
    #     ["P5", 12, 6, 1]
    # ]

    # processes_list = [
    #     ["P1", 3, 4],
    #     ["P2", 5, 9],
    #     ["P3", 8, 4],
    #     ["P4", 0, 7],
    #     ["P5", 12, 6]
    # ]

    # processes_list = [
    #     ["P1", 3, 4, 2, 1],
    #     ["P2", 5, 9, 1, 1],
    #     ["P3", 8, 4, 2, 2],
    #     ["P4", 0, 7, 1, 2],
    #     ["P5", 12, 6, 1, 1]
    # ]

    # processes_list = []

    processes_list = [
        ["P1", 4, 12, 2, 3],
        ["P2", 2, 10, 1, 1],
        ["P3", 65, 3, 2, 2],
        ["P4", 26, 4, 1, 2],
        ["P5", 50, 6, 1, 1],
        ["P6", 20, 2, 2, 3],
        ["P7", 33, 5, 1, 1],
        ["P8", 5, 7, 1, 2],
        ["P9", 108, 2, 2, 3],
        ["P10", 93, 5, 1, 3],
        ["P11", 160, 7, 1, 2],
        ["P12", 135, 10, 1, 1],
        ["P13", 142, 7, 2, 3],
        ["P14", 138, 9, 1, 3],
        ["P15", 140, 7, 1, 2],
        ["P16", 241, 7, 1, 2],
        ["P17", 220, 10, 1, 1],
        ["P18", 213, 7, 2, 1],
        ["P19", 213, 6, 1, 3],
        ["P20", 243, 7, 1, 2],
    ]
    # 4 2 65 26 50 20 33 5 108 93 160 135 142 138 140 241 220 213 213 243
    # 12 10 3 4 6 2 5 7 2 5 7 10 7 9 7 7 10 7 6 7
    # 2 1 2 1 1 2 1 2 2 1 1 1 2 1 1 1 1 2 1 1
    # 3 1 2 2 1 3 1 2 3 3 2 1 3 3 2 2 1 1 3 2

    # processes_list = [
    #     ["P1", 6, 34, 1, 2]
    # ]

    # processes_list = [
    #     ["P1", 3, 4, 2, 1],
    #     ["P2", 5, 9, 1, 1],
    #     ["P3", 8, 4, 2, 2],
    #     ["P4", 0, 7, 1, 2],
    #     ["P5", 12, 6, 1, 1],
    #     ["P6", 5, 2, 1, 3],
    #     ["P7", 18, 7, 2, 3],
    #     ["P8", 10, 8, 1, 1],
    #     ["P9", 2, 1, 2, 3],
    #     ["P10", 14, 9, 1, 3]
    # ]

    # with levels only
    # processes_list = [
    #     ["P1", 3, 4, 1],
    #     ["P2", 5, 9, 1],
    #     ["P3", 8, 4, 2],
    #     ["P4", 0, 7, 2],
    #     ["P5", 12, 6, 1]
    # ]

    # processes_list = [
    #     ["P1", 10, 1, 1],
    #     ["P2", 9, 2, 2],
    #     ["P3", 12, 4, 2],
    #     ["P4", 4, 3, 1],
    #     ["P5", 40, 5, 1],
    #     ["P6", 21, 6, 1],
    #     ["P7", 21, 6, 1]
    # ]

    # for sublist in plist:
    #     print(sublist)

    def __init__(self, main_algo, *algos):
        self.fcfs = main_algo == "FCFS"
        self.time = 0
        self.queue = []

        self.algorithms = {}
        self.colET = 3  # default column number of Ending Time
        self.colTAT = 4  # default column number of Turnaround Time
        self.QT = None
        self.timestamps = [0]
        self.orderOfProcesses = []
        self.min_process = None

        # for MLFQ
        self.mlfq_qt = []
        self.mlfq_levels = None
        self.mlfq_queues = []
        self.mlfq_timestamps = []
        self.mlfq_orderOfProcesses = []

        self.prio_check = False
        self.multi_check = False
        self.multi_feedback_check = False

        self.plist = []

        # if len(algos) > 1 or len(self.algo3) > 1:
        if main_algo == "MLFQ":
            self.multi_feedback_check = True
        if "Priority" in main_algo:
            self.prio_check = True
        if main_algo == "MLQ" or len(algos) > 1:
            self.multi_check = True
        for idx, algo in enumerate(algos):
            self.algorithms[idx + 1] = algo
            if not self.prio_check and "Priority" in algo:
                self.prio_check = True
            # if not self.multi_feedback_check and "MLFQ" in algo:
            #     self.multi_feedback_check = True
        # for algo in self.algo3.values():
        #     if not self.prio_check and "Priority" in algo:
        #         self.prio_check = True
        #         break
        # print(self.prio_check)
        # print(f"colET: {self.colET}")
        # print(f"colTAT: {self.colTAT}")

    def trimProcessList(self):
        # create a copy of processes_list to retain the original value of the given processes data.
        # otherwise, using processes_list in priority algorithms will alter the burst time of the processes,
        # so we create plist, a copy of processes list.
        if self.multi_check and self.prio_check:
            self.plist = sorted(
                copy.deepcopy(self.processes_list),
                key=lambda x: (x[1], x[4], x[3], x[2], x[0]),
            )
        elif self.multi_check or self.prio_check:
            self.plist = sorted(
                copy.deepcopy(self.processes_list),
                key=lambda x: (x[1], x[3], x[2], x[0]),
            )
        else:
            if self.fcfs:
                self.plist = sorted(
                    copy.deepcopy(self.processes_list), key=lambda x: (x[1], x[0], x[2])
                )
            else:
                self.plist = sorted(
                    copy.deepcopy(self.processes_list), key=lambda x: (x[1], x[2], x[0])
                )
        # for i in self.plist:
        #     print(i)

        if not self.prio_check and not self.multi_check:
            self.processes_list = [sublist[:3] for sublist in self.processes_list]
            self.colET = 3
            self.colTAT = 4
        elif self.prio_check and self.multi_check:
            self.processes_list = [sublist[:5] for sublist in self.processes_list]
            self.colET = 5
            self.colTAT = 6
        elif self.prio_check or self.multi_check:
            self.processes_list = [sublist[:4] for sublist in self.processes_list]
            self.colET = 4
            self.colTAT = 5
        # print(f"This is colET: {self.colET} and colTAT: {self.colTAT} ")

    def displayGanttChart(self):
        print("Gantt Chart:")
        print("| ", end="")
        for i in self.orderOfProcesses:
            print(f"{i: >5} | ", end="")
        print()
        for i in self.timestamps:
            print(f"{i: <8}", end="")

    def calculateTable(self):
        print()
        for i in range(len(self.processes_list)):
            # Calculating turnaround time
            self.processes_list[i].append(
                self.processes_list[i][self.colET] - self.processes_list[i][1]
            )
            # Calculating waiting time
            self.processes_list[i].append(
                self.processes_list[i][self.colTAT] - self.processes_list[i][2]
            )

    def displayTable(self):
        print()
        print("Table:")
        print(f"{'Process': >10} | ", end="")
        print(f"{'Arrival': >10} | ", end="")
        print(f"{'Burst': >10} | ", end="")
        if self.prio_check:
            print(f"{'Priority': >10} | ", end="")
        if self.multi_check:
            print(f"{'Level': >10} | ", end="")
        print(f"{'Ending': >10} | ", end="")
        print(f"{'Turnaround': >10} | ", end="")
        print(f"{'Waiting': >10} | ")
        for sublist in self.processes_list:
            for i in sublist:
                print(f"{i: >10} | ", end="")
            print()

    def displayEfficiency(self):
        print("CPU Utilization: ", end="")
        total = 0
        for i in range(len(self.processes_list)):
            total += self.processes_list[i][2]
        print(f"{round(total / self.timestamps[-1] * 100, 2)}%")

        print("Average Turnaround Time: ", end="")
        total = 0
        for i in range(len(self.processes_list)):
            total += self.processes_list[i][self.colTAT]
        print(total / len(self.processes_list))

        print("Average Waiting Time: ", end="")
        total = 0
        for i in range(len(self.processes_list)):
            total += self.processes_list[i][self.colTAT + 1]
        print(total / len(self.processes_list))

    def displayQueue(self):
        print()
        for sublist in self.queue:
            print(sublist)

    # for MLFQ
    def displayMLFQGanttCharts(self):
        for i in range(self.mlfq_levels):
            print()
            if i == self.mlfq_levels - 1:
                print(f"Gantt Chart {i + 1} (Algorithm/s = {self.algorithms}):")
            else:
                print(f"Gantt Chart {i + 1} (Time Slice = {self.mlfq_qt[i]}):")
            print("| ", end="")
            for j in self.mlfq_orderOfProcesses[i]:
                print(f"{j: >5} | ", end="")
            print()
            for j in self.mlfq_timestamps[i]:
                print(f"{j: <8}", end="")
