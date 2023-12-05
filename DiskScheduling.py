def DiskScheduling(inputData):
    algorithm = inputData["diskSchedulingAlgorithm"]
    # if algorithm == "FCFS":
    #     return inputData
    if algorithm == "SSTF":
        inputData["diskRequests"] = SSTF(inputData["diskRequests"])
    elif algorithm == "SCAN":
        inputData["diskRequests"] = SCAN(inputData["diskRequests"])

    return inputData


def SSTF(diskRequests):
    for trav in range(1, len(diskRequests) - 1):
        currValue = diskRequests[trav - 1]
        minDifference = 100000
        for i in range(trav, len(diskRequests)):
            diff = abs(diskRequests[i] - currValue)
            if minDifference > diff:
                minDifference = diff
                minIdx = i
        # swap
        diskRequests[trav], diskRequests[minIdx] = (
            diskRequests[minIdx],
            diskRequests[trav],
        )

    return diskRequests


def SCAN(diskRequests):
    pass
