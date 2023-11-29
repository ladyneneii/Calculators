import copy


def PageReplacement(pageReplacementAlgorithm, pageReferences, numberOfFrames):
    print(pageReplacementAlgorithm)
    print(pageReferences)
    print(numberOfFrames)

    numberOfFrames = int(numberOfFrames)
    frames = [[] for _ in range(numberOfFrames)]
    hitOrFault = []
    replacedRows = []

    # initialize frames
    frames[0].append(pageReferences[0])
    for x in range(1, numberOfFrames):
        frames[x].append("_")
    hitOrFault.append("F")
    remark = "None."
    replacedRows.append({"col": 0, "row": "_"})

    framesDetailsSet = []

    framesDetails = {
        "frames": frames,
        "hitOrFault": hitOrFault,
        "remark": remark,
        "replacedRows": replacedRows,
    }
    framesDetailsSet.append(framesDetails)

    count = {}
    existingPages = []

    for y in range(1, len(pageReferences)):
        frames = copy.deepcopy(frames)
        hitOrFault = copy.deepcopy(hitOrFault)
        replacedRows = copy.deepcopy(replacedRows)
        currentPage = pageReferences[y]
        doesExist = False

        # check if the page exists
        for z in range(numberOfFrames):
            latestPage = frames[z][-1]
            if latestPage == currentPage:
                doesExist = True
            # append the frames with the latest pages. if it is a fault, the appropriate page will be replaced later
            frames[z].append(latestPage)
            if latestPage != "_":
                if not latestPage in existingPages:
                    existingPages.append(latestPage)
                if not latestPage in count:
                    count[latestPage] = 1

        if not doesExist:
            # currentPage does not exist, so it is a fault
            if len(existingPages) >= numberOfFrames:
                if pageReplacementAlgorithm == "FIFO":
                    indexReplace = FIFO(y, frames, numberOfFrames)
                elif pageReplacementAlgorithm == "LRU":
                    indexReplace = LRU(y, pageReferences, existingPages)
                elif pageReplacementAlgorithm == "LFU":
                    indexReplace = LFU(y, frames, count, existingPages)
                elif pageReplacementAlgorithm == "Optimal":
                    indexReplace = Optimal(
                        y, pageReferences, frames, numberOfFrames, existingPages
                    )

                remark = f"{frames[indexReplace][-1]} replaced by {currentPage}."
                existingPages[indexReplace] = currentPage
                # replace the number replaced by the algorithm
                frames[indexReplace][-1] = currentPage
                replacedRows.append({"col": y, "row": indexReplace})
            else:
                for z in range(numberOfFrames):
                    if frames[z][y] == "_":
                        frames[z][y] = currentPage
                        break
                remark = "None."
                replacedRows.append({"col": y, "row": "_"})

            hitOrFault.append("F")
        else:
            # currentPage exists in either of the frames, so it is a hit
            hitOrFault.append("H")
            remark = "None"
            replacedRows.append({"col": y, "row": "_"})

            if pageReplacementAlgorithm == "LFU":
                count[currentPage] += 1

        framesDetails = {
            "frames": frames,
            "hitOrFault": hitOrFault,
            "remark": remark,
            "replacedRows": replacedRows,
        }
        framesDetailsSet.append(framesDetails)

    # calculate hits and faults
    numberOfHits = hitOrFault.count("H")
    numberOfFaults = hitOrFault.count("F")
    hitsPercentage = numberOfHits / len(pageReferences) * 100
    faultsPercentage = numberOfFaults / len(pageReferences) * 100

    statistics = {
        "numberOfHits": numberOfHits,
        "numberOfFaults": numberOfFaults,
        "hitsPercentage": hitsPercentage,
        "faultsPercentage": faultsPercentage,
    }

    # print(framesDetailsSet)
    # print(statistics)

    return framesDetailsSet, statistics


def FIFO(y, frames, numberOfFrames):
    minIndex = 1000  # initialization
    for x in range(numberOfFrames):
        # get the preceding column index of -1, which is -2 in this case. positive indices are used instead of negative ones so that we can check if the index is already out of bounds (the first condition).
        trav = y - 1
        while trav > 0 and frames[x][trav] == frames[x][trav - 1]:
            trav -= 1

        if minIndex > trav:
            minIndex = trav
            indexReplace = x

    return indexReplace


def LRU(y, pageReferences, existingPages):
    visitedPages = []
    trav = y - 1
    while trav >= 0 and len(visitedPages) != len(existingPages):
        page = pageReferences[trav]
        if not page in visitedPages and page in existingPages:
            visitedPages.append(page)
        trav -= 1

    # the last value of visitedPages[] is the least recently used
    # since the values of frames[] appear in the same order as the values of existingPages[], .index() can be used on existingPages to determine the frames[] row index of the desired value
    indexReplace = existingPages.index(visitedPages[-1])

    return indexReplace


def LFU(y, frames, count, existingPages):
    # get all keys with the least value
    min_value = min(count.values())
    keys_with_min_value = [key for key, value in count.items() if value == min_value]

    if len(keys_with_min_value) > 1:
        # there are multiple pages that are least recently used, so use FIFO as the basis.
        minIndex = 1000  # initialization
        for x in range(len(keys_with_min_value)):
            frameIndex = existingPages.index(keys_with_min_value[x])
            trav = y - 1
            while trav > 0 and frames[frameIndex][trav] == frames[frameIndex][trav - 1]:
                trav -= 1

            if minIndex > trav:
                minIndex = trav
                indexReplace = frameIndex
        # keys_with_min_value now only contains the key with the least value and the first to go in (FIFO)
        keys_with_min_value = [existingPages[indexReplace]]

    else:
        indexReplace = existingPages.index(keys_with_min_value[0])

    # delete key
    count.pop(keys_with_min_value[0])

    return indexReplace


def Optimal(y, pageReferences, frames, numberOfFrames, existingPages):
    visitedPages = []
    trav = y + 1
    while trav < len(pageReferences) and len(visitedPages) < len(existingPages):
        page = pageReferences[trav]
        if not page in visitedPages and page in existingPages:
            visitedPages.append(page)
        trav += 1
    print(visitedPages)

    if len(visitedPages) == len(existingPages):
        # the last value of visitedPages[] is the furthest
        # since the values of frames[] appear in the same order as the values of existingPages[], .index() can be used on existingPages to determine the frames[] row index of the desired value
        indexReplace = existingPages.index(visitedPages[-1])
    elif len(visitedPages) < len(existingPages):
        for x in range(len(existingPages)):
            if existingPages[x] not in visitedPages:
                break
        indexReplace = x
    elif len(visitedPages) == 0:
        minIndex = 1000  # initialization
        for x in range(numberOfFrames):
            trav = y - 1
            while trav > 0 and frames[x][trav] == frames[x][trav - 1]:
                trav -= 1

            if minIndex > trav:
                minIndex = trav
                indexReplace = x

    return indexReplace
