import csv
import math
import sys
sys.dont_write_bytecode = True

from collections import Counter

from math import cos, asin, sqrt

from ContiguityClasses import CSDNode, SLAGroup, CSDCluster
from ContiguityUtility import *
from ContiguityFixes import *

fname1 = "SLA_RuralOnly.csv"
fname2 = "CSDNeighbors2.csv"

outputname = "test"

SLADict = None
def main():
    global SLADict
    CSDArray = []
    SLACSDs = csv.DictReader(open(fname1))
    for row in SLACSDs:     CSDArray.append(row)

    infoArray = []
    CSDInfo = csv.DictReader(open(fname2))
    for row in CSDInfo:     infoArray.append(row)

    mArray = leftMergeDictArray(infoArray, CSDArray, "CSDUID", "csd2016")
    outputDictArray(mArray, outputname)

    CSDDict = {}
    SLADict = {}
    SLACSDs = []
    a = 0
    for c in mArray:
        a += 1
        CSD  = CSDNode(c)
        if CSD.SLACode > 0:
            if CSD.SLACode not in SLADict.keys():   SLADict[CSD.SLACode] = SLAGroup(CSD.SLACode)
            SLADict[CSD.SLACode].addCSD(CSD)
            SLACSDs.append(CSD)
        #if a > 10: break
        CSDDict[CSD.CSDCode] = CSD

    CMACACodes = ["996","997","998", "999", "0"]

    #----------------------------------------------
    unassigned = updateNodes(CSDDict)
    print str(len(unassigned)) + " unassigned left"
    #---------------------------------------------

    splitSLAs(SLACSDs, CSDDict, unassigned)     #Assign single CSDs separated from SLA either by singly empty CSD or all other SLAs

    #---------------------------------------------
    unassigned = updateNodes(CSDDict)
    print str(len(unassigned)) + " unassigned left"
    #---------------------------------------------

    complexSplitSLAs(SLADict, CSDDict)

    #---------------------------------------------
    unassigned = updateNodes(CSDDict)
    print str(len(unassigned)) + " unassigned left"
    #----------------------------------------------
    #LAST CLEANUP - PUT SURROUNDED EMPTIES AND EMPTY SURROUNDED CLUSTERS WITH SLAS

    unassigned = surroundedEmpties(unassigned)  #Assign non-assigned CSDs surrounded wholly by SLAs
    surroundedClusters(CSDDict, SLADict)  #Assign non-assigned CSDs surrounded wholly by SLAs
    #ADD FUNCTION FOR FINAL ASSIGNING OF EMPY TO CLUSTERS


    #---------------------------------------------
    unassigned = updateNodes(CSDDict)
    print str(len(unassigned)) + " unassigned left" #Final ount should be 0
    #---------------------------------------------

    outputCSDs(CSDDict, "contiguityOutput")



def updateNodes(CSDDict):
    global SLADict
    SLADict = {}
    unassigned = []
    for key, value in CSDDict.items():
        value.updateNodes(CSDDict)
        if value.SLACode == 0  and not value.CMACA:
            unassigned.append(value)
        elif value.SLACode >0:
            if value.SLACode not in SLADict.keys():   SLADict[value.SLACode] = SLAGroup(value.SLACode)
            SLADict[value.SLACode].addCSD(value)
    return unassigned

def surroundedClusters(CSDDict, SLADict):
    simpleCount = 0
    simpleCSDs = 0

    SLADict[0] = SLAGroup(0)
    emptyGroup = SLADict[0]
    for key, value in CSDDict.items():
        if value.SLACode == 0 and not value.CMACA: emptyGroup.addCSD(value)
    emptyGroup.makeClusters()
    print len(emptyGroup.CSDClusters), "Empty CSD Clusters"

    for cluster in emptyGroup.CSDClusters:
        SLAs = []

        if len(cluster.neighbors) == len(cluster.SLANeighbors):
            for CSD in cluster.SLANeighbors:
                if CSD.SLACode not in SLAs: SLAs.append(CSD.SLACode)
        if len(SLAs) == 1:
            SLACode = SLAs[0]
            for i in cluster.CSDs:
                i.SLACode = SLACode
                i.changed = True
                i.changeType = "10 - Simple Surrounded Empty Cluster"
                simpleCSDs += 1
            simpleCount += 1

    print str(simpleCount) + " empty cluster surrounded fixed - ", simpleCSDs,"CSDs"

    SLADict[0] = SLAGroup(0)
    emptyGroup = SLADict[0]
    for key, value in CSDDict.items():
        if value.SLACode == 0 and not value.CMACA: emptyGroup.addCSD(value)
    emptyGroup.makeClusters()
    code = 999990
    for cluster in emptyGroup.CSDClusters:
        prov = []
        for CSD in cluster.CSDs:
            pr = CSD.CSDCode[:2]
            if pr not in prov: prov.append(pr)
        for p in prov:
            for CSD in cluster.CSDs:
                pr = CSD.CSDCode[:2]
                if p == pr:
                    CSD.SLACode = code
            code +=1


def surroundedEmpties(array):
    simpleCount = 0
    twoCount = 0
    newArray = []
    for i in array:
        solved = False
        if len(i.NonSLANeighbors) == 0 and len(i.SLANeighbors) > 0:
            #Check to see if simplest case
            codes = []
            for n in i.SLANeighbors:
                if n.SLACode not in codes: codes.append(n.SLACode)
            if(len(codes) == 1):
                i.SLACode = i.SLANeighbors[0].SLACode
                i.changed = True
                i.changeType = "1 - Simple Surrounded Single CSD"
                solved = True
                simpleCount += 1
            else:
                newCode = assignToAdjacent(i)
                if i.CSDCode == "4815045":
                    print "assign to adjacent", len(codes), newCode
                if(newCode>0):
                    i.SLACode = newCode
                    i.changeType = "2 - Complex Surrounded Single CSD"
                    twoCount += 1

        if not solved: newArray.append(i)

    print str(simpleCount) + " simple surrounded fixed"
    print str(twoCount) + " complex surrounded fixed"
    return newArray

def splitSLAs(array, CSDDict, unassigned):
    simpleCount = 0
    islandCount = 0
    island2Count = 0

    directNeighbor = 0

    for i in array:
        changed = False
        if len(i.mySLANeighbors) == 0:
            simpleCount +=1
            if len(i.SLANeighbors) == len(i.neighbors):
                newCode = assignToAdjacent(i)
                if newCode > 0:
                    i.SLACode = newCode
                    islandCount += 1
                    i.changeType = "3 - Isolated SLA part assigned to adjacent"
                    changed = True
            singleBridge = findSinglePath(i)
            if(singleBridge != 0):
                directNeighbor += 1
                singleBridge.SLACode = i.SLACode
                singleBridge.changeType = "4 - Bridge CSD to make SLA contiguous"
                changed = True
        if changed: updateNodes(CSDDict)

    print (str(simpleCount) + " isolated SLA CSDs")
    print (str(islandCount) + " Isolated SLA part assigned to adjacent SLA")

    print (str(directNeighbor) + " Isolated SLA part solved by single bridge CSD")

def complexSplitSLAs(SLADict, CSDDict):
    bridges1 = 0
    bridges2 = 0
    split = []
    for key, value in SLADict.items():
        test = value.makeClusters()
        if test != 0: split.append(test)

    for SLA in split:
        changed = False
        info = str(SLA.SLACode) + ": "
        for cluster in SLA.CSDClusters:
            info += str(len(cluster.CSDs)) + "-"
        if len(SLA.CSDClusters) == 2:
            minDistance = 1000000000000
            cluster1 = SLA.CSDClusters[0]
            cluster2 = SLA.CSDClusters[1]
            for CSD1 in cluster1.CSDs:
                for CSD2 in cluster2.CSDs:
                    d = distance(CSD1.CSDLat, CSD1.CSDLong, CSD2.CSDLat, CSD2.CSDLong)
                    if d<minDistance: minDistance = d
            if minDistance > 200: print "!!!! - Long distance SLA showed up", SLA.SLACode, minDistance
            else:
                singleBridge = findSinglePathClusters(cluster1, cluster2)
                if singleBridge != 0:
                    bridges1 += 1
                    singleBridge.SLACode = SLA.SLACode
                    singleBridge.changeType = "4 - Bridge CSD to make SLA contiguous"
                    changed = True
                else:
                    doubleBridge = findDoublePathClusters(cluster1, cluster2)
                    if doubleBridge != 0:
                        bridges2 += 1
                        for CSD in doubleBridge:
                            CSD.SLACode = SLA.SLACode
                            CSD.changeType = "5 - DoubleBridge CSD to make SLA contiguous"
                        changed = True
        elif len(SLA.CSDClusters) == 3:
            cluster1 = SLA.CSDClusters[0]
            cluster2 = SLA.CSDClusters[1]
            cluster3 = SLA.CSDClusters[2]
            singleBridge = findSinglePathClusters(cluster1, cluster2)
            if singleBridge != 0:
                bridges1 += 1
                singleBridge.SLACode = SLA.SLACode
                singleBridge.changeType = "4 - Bridge CSD to make SLA contiguous"
                changed = True
                updateNodes(CSDDict)
            else:
                singleBridge = findSinglePathClusters(cluster1, cluster3)
                if singleBridge != 0:
                    bridges1 += 1
                    singleBridge.SLACode = SLA.SLACode
                    singleBridge.changeType = "4 - Bridge CSD to make SLA contiguous"
                    changed = True
                    updateNodes(CSDDict)
            SLA.makeClusters()
            if len(SLA.CSDClusters) > 1:
                singleBridge = findSinglePathClusters(cluster2, cluster3)
                if singleBridge != 0:
                    bridges1 += 1
                    singleBridge.SLACode = SLA.SLACode
                    singleBridge.changeType = "4 - Bridge CSD to make SLA contiguous"
                    changed = True
                    updateNodes(CSDDict)
            SLA.makeClusters()
        if changed: updateNodes(CSDDict)

    split = []
    for key, value in SLADict.items():
        test = value.makeClusters()
        if test != 0: split.append(test)


    for SLA in split:
        info = str(SLA.SLACode) + "   "
        smallestClust = 0
        smallestClustPop = 10000000000000000
        for clust in SLA.CSDClusters:
            info += str(len(clust.CSDs)) + "-"+ str(len(clust.neighbors))+ "-"+ str(len(clust.SLANeighbors))
            info += "-" + str(clust.pop) + "   "
            if clust.pop < smallestClustPop:
                smallestClust = clust
                smallestClustPop = clust.pop
        if smallestClust != 0:
            if len(smallestClust.neighbors) == 0 or len(smallestClust.SLANeighbors) == 0:
                for CSD in SLA.CSDs:
                    CSD.changeType = "6 - Split Without Neighbors or Without SLA Neighbors to Dissolve"
            #print 1
        #print info

    print ("number of split SLAs ", len(split))
    print ("number of single-bridged Clusters ", bridges1)
    print ("number of double-bridged Clusters ", bridges2)

if __name__ == '__main__':
    main()