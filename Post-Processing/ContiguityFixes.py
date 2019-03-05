from collections import Counter


def findSinglePathClusters(c1, c2):
    SLA = c1.SLAObject
    possibleBridges = []
    for n in c1.NonSLANeighbors:
        for n1 in c2.NonSLANeighbors:
            if n == n1 and n not in possibleBridges:
                possibleBridges.append(n)

    if len(possibleBridges) == 1: return possibleBridges[0]
    elif len(possibleBridges) > 1:
        bridge = 0
        smallestArea = 10000000000000000000
        for b in possibleBridges:
            if b.CSDArea <  smallestArea:
                smallestArea = b.CSDArea
                bridge = b
        return bridge
    return 0



def findDoublePathClusters(c1, c2):
    SLA = c1.SLAObject
    possibleBridges = []
    foundLink = []
    bridgePairs = []
    for n in c1.NonSLANeighbors:
        if n not in possibleBridges: possibleBridges.append(n)
    for n in possibleBridges:
        for n2 in n.NonSLANeighbors:
            if n2 not in possibleBridges: possibleBridges.append(n2)

    for n in possibleBridges:
        for n1 in c2.NonSLANeighbors:
            if n == n1 and n not in foundLink:
                foundLink.append(n)
                for n2 in c1.NonSLANeighbors:
                    if n2 in n.NonSLANeighbors:
                        bridgePairs.append([n, n2])

    if len(bridgePairs) == 1: return bridgePairs[0]
    return 0

def findSinglePath(CSD):
    SLA = CSD.SLAObject
    possibleBridges = []
    for n in CSD.NonSLANeighbors:
        for c in SLA.CSDs:
            if c == CSD: continue
            for ntest in c.neighbors:
                if ntest not in c.SLANeighbors:
                    if n == ntest and n not in possibleBridges: possibleBridges.append(n)
    if len(possibleBridges) == 1: return possibleBridges[0]
    elif len(possibleBridges) > 1:
        bridge = 0
        smallestArea = 10000000000000000000
        for b in possibleBridges:
            if b.CSDArea <  smallestArea:
                smallestArea = b.CSDArea
                bridge = b
        return bridge
    return 0

def assignToAdjacent(CSD): #Takes a CSD and assigns it by CD or by largest population center. Returns new code
    codes = []
    sla = []
    for n in CSD.SLANeighbors:
        if n.SLACode not in codes:
            codes.append(n.SLACode)
            sla.append(n.SLAObject)

    myCode = CSD.CDCode

    if(len(codes) < 10):
        CDCodes = []
        for a in range(0, len(codes)):
            code = codes[a]
            tempCD = []
            for n in CSD.SLANeighbors:
                if n.SLACode == code:
                    tempCD.append(n.CDCode)
                    cnt = Counter(tempCD)
            CDCodes.append(cnt.most_common(1)[0][0])
        for s in sla:
            tempCD = []
            for csd in s.CSDs:
                tempCD.append(csd.CDCode)
            cnt = Counter(tempCD)
            s.CDMode = cnt.most_common(1)[0][0]

        matches = 0
        mArray = []
        for a in range(0, len(codes)):
            code = CDCodes[a]
            if code == myCode:
                matches += 1
                mArray.append(codes[a])
        if matches == 1:
            for a in range(0, len(codes)):
                code = CDCodes[a]
                if code == myCode:
                    return codes[a]
        else:
            found = 0
            foundSLA = 0
            for s in sla:
                if s.CDMode == myCode:
                    found +=1
                    foundSLA = s
            if found == 1: return foundSLA.SLACode
            else:
                largestPop = 0
                newCode = 0
                for s in sla:
                    for CSD in s.CSDs:
                        if CSD.CSDPop > largestPop:
                            largestPop = CSD.CSDPop
                            newCode = s.SLACode
                return newCode

    return 0