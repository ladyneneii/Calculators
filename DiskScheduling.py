def DiskScheduling(inputData):
    algorithm = inputData["diskSchedulingAlgorithm"]
    # if algorithm == "FCFS":
    #     return inputData
    if algorithm == "SSTF":
        inputData["diskRequests"] = SSTF(inputData["diskRequests"])
    elif algorithm == "SCAN":
        inputData["diskRequests"] = SCAN(
            inputData["diskRequests"], int(inputData["numberOfCylinders"])
        )
    elif algorithm == "C-SCAN":
        inputData["diskRequests"] = CSCAN(
            inputData["diskRequests"], int(inputData["numberOfCylinders"])
        )
    elif algorithm == "LOOK":
        inputData["diskRequests"] = LOOK(inputData["diskRequests"])
    elif algorithm == "C-LOOK":
        inputData["diskRequests"] = CLOOK(inputData["diskRequests"])

    inputData["seekTime"] = calculateSeekTime(inputData["diskRequests"])

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


def SCAN(diskRequests, numberOfCylinders):
    firstNum = diskRequests[0]
    ascendArr = [firstNum, numberOfCylinders - 1]
    descendArr = []
    for i in range(1, len(diskRequests)):
        if firstNum < diskRequests[i]:
            ascendArr.append(diskRequests[i])
        else:
            descendArr.append(diskRequests[i])
    ascendArr.sort()
    descendArr.sort(reverse=True)

    return ascendArr + descendArr


def CSCAN(diskRequests, numberOfCylinders):
    firstNum = diskRequests[0]
    ascendArr = [firstNum, numberOfCylinders - 1]
    ascendArr2 = [0]
    for i in range(1, len(diskRequests)):
        if firstNum < diskRequests[i]:
            ascendArr.append(diskRequests[i])
        else:
            ascendArr2.append(diskRequests[i])
    ascendArr.sort()
    ascendArr2.sort()

    return ascendArr + ascendArr2


def LOOK(diskRequests):
    firstNum = diskRequests[0]
    ascendArr = [firstNum]
    descendArr = []
    for i in range(1, len(diskRequests)):
        if firstNum < diskRequests[i]:
            ascendArr.append(diskRequests[i])
        else:
            descendArr.append(diskRequests[i])
    ascendArr.sort()
    descendArr.sort(reverse=True)

    return ascendArr + descendArr


def CLOOK(diskRequests):
    firstNum = diskRequests[0]
    ascendArr = [firstNum]
    ascendArr2 = []
    for i in range(1, len(diskRequests)):
        if firstNum < diskRequests[i]:
            ascendArr.append(diskRequests[i])
        else:
            ascendArr2.append(diskRequests[i])
    ascendArr.sort()
    ascendArr2.sort()

    return ascendArr + ascendArr2


def calculateSeekTime(diskRequests):
    seek_time = 0

    for i in range(1, len(diskRequests)):
        seek_time += abs(diskRequests[i] - diskRequests[i - 1])

    return seek_time
