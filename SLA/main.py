
import csv
import math
import sys

endArea = 4574
lastClusterID = 4574

areaArray = 0
outputFilesB = False


"""declarative constants for success criteria and population threshold"""
lowestPop = 0           #lowest population threshold"""
highSelf = .90          #self-containment required for small areas"""
highestPop = 25000      #highest population threshold"""
lowSelf = .75           #lowest self-containment required"""

minFlow = 20
inputName = 'test'
fname = 'test'

slope = (-highSelf+lowSelf)/(highestPop - lowestPop)      #The decrease in required self-containment as areas grow smaller. """
modifier = highSelf - (slope*lowestPop)                   #A modifier that's always equal to the highest level of self-containment if the lowest threshold is 0. """

nextUnsuccessfulArea = 0
eligibleTypes = [0, 2]
ineligibleTypes = [1, 4]

removedAreas = []
noMatch = []
"""TYPES:
    0 - not clustered
    1 - clustered CSD
    2 - not clustered cluster
    4 - clustered cluster, used for tracking"""

def runSLAs():
    global areaArray, noMatch,k, inputName
    input_file = csv.DictReader(open(inputName))

    areaArray = []
    for i in range(1, endArea+1):       #Create an empty array for the flows and populate it with empty dictionary objects
        pDict = {"area": i, "RELF": 0, "WELF": 0, "RW": 0, "TYPE": 0, "SUCCEEDED":0, "DISTANCE": 0, "NOTE": "", "CLUSTER": 0, "AREAA": 0, "AREAB":0, "CMA": -1}
        areaArray.append(pDict)
        for j in range(1, endArea+1):       pDict[j] = 0

    for row in input_file:              #Fill the dictionary with information from the relevant flows
        resA = int(row["RES"])
        powA = int(row["POW"])
        flow = int(row["TotalFlow"])
        if flow < minFlow: flow = 0
        resDict = areaArray[resA - 1]
        powDict = areaArray[powA - 1]

        try:
            if row["RESCMA"] != "0" or row["POWCMA"] != "0": flow = 0
            resDict["CMA"] = row["RESCMA"]
            powDict["CMA"] = row["POWCMA"]
        except:
            resDict["CMA"] = "0"
            powDict["CMA"] = "0"

        resDict["RELF"] += flow
        resDict[powA] = flow
        if(resA == powA): resDict["RW"] += flow
        powDict["WELF"] += flow


    if outputFilesB: outputFiles()
    numReps = 5000
    tracking = 0
    allSuccess = False

    noMatch = []
    while tracking < numReps and not allSuccess:
        tracking +=1
        size = 0
        calculateSuccess()
        if nextUnsuccessfulArea == 0:      allSuccess = True
        else:
            match = searchStrength()
            if(match == 0): noMatch.append(nextUnsuccessfulArea)
            else:           clusterAreas(nextUnsuccessfulArea, match)
    outputClusters()
    print "done!", lastClusterID, tracking

def outputClusters():
    filename = fname + '.csv'
    f = open(filename,'w')
    line = "area,type,cluster,succeeded,RELF,WELF,RW,SEEKING,MATCH"
    f.write(line +'\n')

    for a in range(0, len(areaArray)):
        newA = areaArray[a]
        area = a+1
        type = newA["TYPE"]
        cluster = newA["CLUSTER"]
        succeeded = newA["SUCCEEDED"]
        if succeeded == 1 and type == 0: succeeded = 5   #If it's only a single CSD, mark it as a special success.
        RELF = newA["RELF"]
        WELF = newA["WELF"]
        RW = newA["RW"]
        AREAA = newA["AREAA"]
        AREAB = newA["AREAB"]
        line = str(area) + "," + str(type)  + "," + str(cluster) + "," + str(succeeded) + "," + str(RELF) + "," + str(WELF) + "," + str(RW) + "," + str(AREAA) + "," + str(AREAB)
        f.write(line)
        f.write('\n')
    f.close()

    filename = fname + '_CSDS.csv'
    f = open(filename,'w')
    line = "area,type,cluster,succeeded,RELF,WELF,RW,CMA"
    f.write(line +'\n')

    for a in range(0, len(areaArray)):
        newA = areaArray[a]
        area = a+1
        type = newA["TYPE"]
        cluster = newA["CLUSTER"]
        succeeded = newA["SUCCEEDED"]
        if succeeded == 1 and type == 0: succeeded = 5   #If it's only a single CSD, mark it as a special success.
        RELF = newA["RELF"]
        WELF = newA["WELF"]
        RW = newA["RW"]
        if(type == 0 or type == 1):
            line = str(area) + "," + str(type)  + "," + str(cluster) + "," + str(succeeded) + "," + str(RELF) + "," + str(WELF) + "," + str(RW) + "," + str(newA["CMA"])
            f.write(line)
            f.write('\n')
    f.close()

    filename = fname + '_CLUSTERS.csv'
    f = open(filename,'w')
    line = "area,type,cluster,succeeded,RELF,WELF,RW"
    f.write(line +'\n')

    for a in range(0, len(areaArray)):
        newA = areaArray[a]
        area = a+1
        type = newA["TYPE"]
        cluster = newA["CLUSTER"]
        succeeded = newA["SUCCEEDED"]
        if succeeded == 1 and type == 0: succeeded = 5   #If it's only a single CSD, mark it as a special success.
        RELF = newA["RELF"]
        WELF = newA["WELF"]
        RW = newA["RW"]
        if(type == 2):
            line = str(area) + "," + str(type)  + "," + str(cluster) + "," + str(succeeded) + "," + str(RELF) + "," + str(WELF) + "," + str(RW)
            f.write(line)
            f.write('\n')
    f.close()


def calculateSuccess():
    global nextUnsuccessfulArea, noMatch
    nextUnsuccessfulArea = 0
    leastSuccess = 0
    for a in range(0, len(areaArray)):
        newA = areaArray[a]
        type = newA["TYPE"]
        if type in eligibleTypes: #If it's an unclustered CSD or 'current' cluster
            areaID = newA["area"]
            RELF, WELF, RW = newA["RELF"], newA["WELF"], newA["RW"]
            WFAway = WELF - RW
            RGAway = RELF - RW
            if(RELF == 0): rSELF, RGAway = 0.0, 0
            else: rSELF = float(RW)/float(RELF)

            if(WELF == 0): wSELF, WFAway = 0.0, 0
            else:
                wSELF = float(RW)/float(WELF)

            #calculate distance from line of success, as defined by the thresholds.  This section is only applied if the RELF is below the lowest threshold, which in this case is 0. Will always be 0.9, since rSELF is 0 and wSELF is 0
            if (RELF <= lowestPop):
                distanceSquaredR = ((lowestPop - RELF)*(lowestPop - RELF)) + ((highSelf-rSELF)*(highSelf-rSELF))
                successR = math.sqrt(distanceSquaredR)
                distanceSquaredW = ((lowestPop - RELF)*(lowestPop - RELF)) + ((highSelf-wSELF)*(highSelf-wSELF))
                successW = math.sqrt(distanceSquaredW)

            #calculate distance from line of success, as defined by the thresholds.  This section is only applied if the RELF is above the highest threshold, which in this case is 25000.
            if (RELF >= highestPop):
                successR = lowSelf - rSELF
                successW = lowSelf - wSELF

            #calculate distance from line of success, as defined by the thresholds.  This section is applied if the RELF is between the thresholds.
            if ((lowestPop < RELF) and (RELF < highestPop)):
                selfCC = (slope*RELF) + modifier
                selfCW = (slope*WELF) + modifier
                successR = selfCC - rSELF
                successW = selfCW - wSELF

            #Calculate combined success on both sides. If either is negative, means it's past success line so distance from success is zero.
            if successR < 0: successR = 0
            if successW < 0: successW = 0
            success = successR + successW

            typeA, succeeded = 0, 0
            #Beginning of checking for success conditions
            #if the area is totally self contained then mark it as special success and skip.
            if ((RW==WELF) and (RW ==RELF)):
                if type == 0:
                    type = 1
                    succeeded = 5
            else:
                #If it is too small mark it as not successful.  This is never applied with the current thresholds, but would allow a minimum size to be set for SLAs.
                if (RELF < lowestPop): succeeded = 0
                else:
                    #If it is not too small check to see if it meets the highest bound - if so, mark as successful
                    if (RELF >= lowestPop and rSELF >= highSelf and wSELF >= highSelf):
                        succeeded = 1;
                    #If it is large enough but does not meet the maximum then see if it is above the minimum
                    else:
                        #If it is above the minimum and thus between the bounds, calculate the acceptable level
                        if (rSELF >= lowSelf and wSELF >= lowSelf):
                            selfCC = (slope*RELF) + modifier
                            selfCW = (slope*WELF) + modifier
                            if (rSELF >= selfCC and wSELF >= selfCW):
                                succeeded = 1        #If it meets the criteria, then it has succeeded.
            if int(newA["CMA"]) > 0: succeeded = 5
            if areaID in noMatch: succeeded = 10
            newA["TYPE"] = type
            newA["SUCCEEDED"] = succeeded
            newA["DISTANCE"]  = success

            if succeeded == 0 and leastSuccess < success:
                nextUnsuccessfulArea = areaID
                leastSuccess = success

def searchStrength():
    seekingArea = areaArray[nextUnsuccessfulArea-1]
    strongestConnection = 0
    strongestArea       = 0
    for a in range(0, len(areaArray)):
        matchArea = areaArray[a]
        type = matchArea["TYPE"]
        if(matchArea != seekingArea and type in eligibleTypes): #if it's a different area and not part of a larger cluster, calculate the strength of the relationship.
            resflow = seekingArea[matchArea["area"]]
            powflow = matchArea[seekingArea["area"]]
            resCMA = seekingArea["CMA"]
            powCMA = matchArea["CMA"]

            if resflow > 0 or powflow > 0:
                RELF, WELF, RW = seekingArea["RELF"], seekingArea["WELF"], seekingArea["RW"]
                RELFP, WELFP, RWP = matchArea["RELF"], matchArea["WELF"], matchArea["RW"]

                if(RELF > 0 and WELFP > 0):     leftCalc = (float(resflow)/float(RELF))*(float(resflow)/float(WELFP)) #(F(a->b)/RELF(a))*(F(a->b)/WELF(b)) - left side, how important a-> b is to a and b
                else:                           leftCalc = 0

                if(RELFP > 0 and WELF > 0):     rightCalc = (float(powflow)/float(RELFP))*(float(powflow)/float(WELF)) #(F(b->a)/RELF(b))*(F(b->a)/WELF(a)). - right side, how important b-> a is to a and b
                else:                           rightCalc = 0
                connection = leftCalc + rightCalc

                if(connection > strongestConnection) and (powCMA == "0" or powCMA == -10) and (resCMA == "0" or resCMA == -10):
                    strongestConnection = connection
                    strongestArea = matchArea["area"]
    return strongestArea

def clusterAreas(seeking, match):
    global lastClusterID, areaArray
    seekingArea = areaArray[seeking-1]
    matchArea = areaArray[match-1]
    newClusterID = lastClusterID + 1
    lastClusterID = newClusterID

    newCluster = {"area": newClusterID, "RELF": 0, "WELF": 0, "RW": 0, "TYPE": 2, "SUCCEEDED":0, "DISTANCE": 0, "NOTE": "", "CLUSTER": 0, "AREAA": seeking, "AREAB": match, "CMA": -10}
    RELF, WELF, RW = 0, 0, 0
    for j in range(1, len(areaArray)+1): #create outflows for new area
        otherArea = areaArray[j-1]
        typeOA = otherArea["TYPE"]
        if(typeOA in eligibleTypes):
            newCluster[j] = seekingArea[j] + matchArea[j]
            RELF += seekingArea[j] + matchArea[j] #CHECK
        else: newCluster[j] = -1

    for k in range(1, len(areaArray)+1): #create inflows for new area
        otherArea = areaArray[k-1]
        typeOA = otherArea["TYPE"]
        if(typeOA in eligibleTypes):
            otherArea[newClusterID] = otherArea[seeking] + otherArea[match]
            WELF += otherArea[seeking] + otherArea[match] #CHECK
        else:
            pass #don't create inflow for areas that have already been set to empty dicts

    RW = seekingArea[seeking] + matchArea[match] + seekingArea[match] + matchArea[seeking] #create RW value for new cluster
    newCluster[newClusterID] = RW
    newCluster["RELF"] = RELF
    newCluster["WELF"] = WELF
    newCluster["RW"] = RW

    print "create new cluster", newClusterID

    for a in range(1, len(areaArray)+1): #tag all associated CSDs and clusters to remove them from later iterations
        area = areaArray[a-1]
        currentCluster = area["CLUSTER"]
        if a == seeking or a == match or currentCluster == seeking or currentCluster == match:
            currentType = area["TYPE"]
            if currentType == 0 or currentType == 1:    #If a CSD belonging to the new cluster or a subcluster, tag it with new ID
                area["CLUSTER"] = newClusterID
                area["TYPE"]    = 1
            if currentType == 2 or currentType == 3:    #If a cluster, tag it with the new cluster.
                area["CLUSTER"] = newClusterID
                area["TYPE"]    = 4

    newSeek  = {"area": seekingArea["area"], "RELF": seekingArea["RELF"], "WELF": seekingArea["WELF"], "RW": seekingArea["RW"], "TYPE": seekingArea["TYPE"], "CLUSTER": seekingArea["CLUSTER"], "AREAA": seekingArea["AREAA"], "AREAB":seekingArea["AREAB"], "SUCCEEDED":seekingArea["SUCCEEDED"], "DISTANCE": 0, "CMA":seekingArea["CMA"], "NOTE":""}
    newMatch = {"area": matchArea["area"], "RELF": matchArea["RELF"], "WELF": matchArea["WELF"], "RW": matchArea["RW"], "TYPE": matchArea["TYPE"], "CLUSTER": matchArea["CLUSTER"], "AREAA": matchArea["AREAA"], "AREAB":matchArea["AREAB"], "SUCCEEDED":matchArea["SUCCEEDED"], "DISTANCE": 0,  "CMA":matchArea["CMA"], "NOTE": ""}
    areaArray[seeking-1] = newSeek
    areaArray[match-1]   = newMatch
    areaArray.append(newCluster)

def outputFiles():
    f = open('flowMatrix.csv','w')
    line = "data"
    for a in range(0, endArea):   line += ", " + str(a+1)
    f.write(line)
    f.write('\n')

    for a in range(0, endArea):
        newA = areaArray[a]
        line = str(newA["area"])
        for j in range(1, endArea+1):
            line += ", "
            line += str(newA[j])
        f.write(line)
        f.write('\n')
    f.close()

    f = open('flowData.csv','w')
    line = "area, RELF, WELF, RW, STATUS, CLUSTER"
    f.write(line)
    f.write('\n')

    for a in range(0, endArea):
        newA = areaArray[a]
        SELF = 0
        line = str(newA["area"]) + ", " + str(newA["RELF"]) + ", " + str(newA["WELF"]) + ", " + str(newA["RW"]) + ", 0, 0"
        f.write(line)
        f.write('\n')

    f.close()

def main(inputFile, numberOfAreas, lowestPopulation=0, highestPopulation=25000, lowestSelfContainment = 0.75, highestSelfContainment = 0.90, outputName = "SLA", minimumFlow = 20):
    global inputName, endArea, lastClusterID, lowestPop, highestPop, lowSelf, highSelf, fname, minFlow, slope, modifier
    inputName = inputFile
    endArea, lastClusterID = numberOfAreas, numberOfAreas
    lowestPop = lowestPopulation
    highestPop = highestPopulation
    lowSelf = lowestSelfContainment
    highSelf = highestSelfContainment
    fname = outputName
    minFlow = minimumFlow

    slope = (-highSelf+lowSelf)/(highestPop - lowestPop)
    modifier = highSelf - (slope*lowestPop)

    runSLAs()

main("ACSDflowsCSV_2011.csv", 3216)
