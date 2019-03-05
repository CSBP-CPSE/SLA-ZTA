class SLAGroup:

    SLACode = 0
    CSDs = []
    CSDClusters = []

    def __init__(self, code):
        self.SLACode = code
        self.CSDs = []
        self.CSDClusters = []
        self.pop = 0

    def addCSD(self, CSD):
        self.CSDs.append(CSD)
        CSD.SLAObject = self
        CSD.SLACode = self.SLACode

    def makeClusters(self):
        self.CSDClusters = []
        CSD = self.CSDs[0]
        self.newCluster(CSD)

        total = 0
        for clust in self.CSDClusters: total += len(clust.CSDs)
        endLoop = False
        a=0
        if total < len(self.CSDs):
            while len(self.CSDs) != total or endLoop:
                inCluster = False
                newSeed = 0
                for c in self.CSDs:
                    inCluster = False
                    for test in self.CSDClusters:
                        if c in test.CSDs: inCluster = True
                    if not inCluster:
                        newSeed = c
                        break
                if newSeed == 0:    endLoop = True
                else:               self.newCluster(newSeed)

                total = 0
                for clust in self.CSDClusters: total += len(clust.CSDs)
        if len(self.CSDClusters) > 1: return self
        return 0

    def newCluster(self, CSD, verbose = False):
        cluster = CSDCluster(self)
        cluster.populateCluster(CSD)
        self.CSDClusters.append(cluster)


class CSDCluster:

    def __init__(self, SLAOb):
        self.originalSLACode = SLAOb.SLACode
        self.SLACode = SLAOb.SLACode
        self.SLAObject = SLAOb
        self.pop = 0

    def populateCluster(self, CSD):
        self.CSDs = []
        self.visit = []

        self.neighborCodes = []
        self.neighbors = []

        self.SLANeighbors = []
        self.NonSLANeighbors = []
        self.mySLANeighbors = []

        self.visit.append(CSD)
        stop = False

        if self.SLACode > 0:
            while not stop:
                c = self.visit[0]
                for n in c.mySLANeighbors:
                    if n not in self.CSDs and n not in self.visit:
                        self.visit.append(n)
                self.CSDs.append(c)
                self.visit.pop(0)
                if len(self.visit) == 0: stop = True
        else:
            while not stop:
                c = self.visit[0]
                for n in c.NonSLANeighbors:
                    if n not in self.CSDs and n not in self.visit:
                        self.visit.append(n)
                self.CSDs.append(c)
                self.visit.pop(0)
                if len(self.visit) == 0: stop = True

        self.pop = 0
        for c in self.CSDs:
            self.pop += c.CSDPop
            for n in c.neighbors:
                if n not in self.neighbors and n not in self.CSDs: self.neighbors.append(n)
                #No MySLA neighbors, because all are in cluster
                if n not in self.CSDs:
                    if n.SLACode == 0 and n not in self.NonSLANeighbors: self.NonSLANeighbors.append(n)
                    if n.SLACode > 0  and n not in self.SLANeighbors: self.SLANeighbors.append(n)

class CSDNode:
    CMACACodes = ["996","997","998", "999", "0"]

    changed = False
    changeType = ""

    CSDCode = 0
    CDCode = 0
    CMACACode = 0
    CMACA = True

    SLACode = 0
    originalSLACode = 0
    SLAObject = 0

    CSDPop = 0
    CSDArea = 0

    neighborCodes = []
    neighbors = []

    SLANeighbors = []
    NonSLANeighbors = []
    mySLANeighbors = []

    def __init__(self, infoD):
        self.CSDCode = str(infoD["CSDUID"])
        self.CDCode = str(infoD["CDUID"])

        self.CMACACode = infoD["CMAuid"]
        if self.CMACACode in self.CMACACodes: self.CMACA = False

        self.SLACode = int(infoD[" cluster"])
        self.originalSLACode = int(infoD[" cluster"])
        if self.SLACode == -1: self.SLACode = 0

        self.neighborCodes = infoD["NEIGHBORS"].split("-")
        if len(infoD["NEIGHBORS2"])>1: self.neighborCodes += infoD["NEIGHBORS2"].split("-")
        if len(infoD["NEIGHBORS3"])>1: self.neighborCodes += infoD["NEIGHBORS3"].split("-")

        self.CSDPop = int(infoD["CSDpop"])
        self.CSDArea = float(infoD["CSDarea"])

        self.CSDLat = float(infoD["CSDlat"])
        self.CSDLong = float(infoD["CSDlong"])

        self.split = False

    def isNeighbor(self, testCSD):
        for n in allNeighborCSDs:
            if testCSD == n: return True
        return False

    def updateNodes(self, dic):
        self.neighbors =[]
        self.SLANeighbors = []
        self.NonSLANeighbors = []
        self.mySLANeighbors = []

        for n in self.neighborCodes:
            if n == "": continue
            nNode = dic[n]
            if nNode.CMACA: continue
            self.neighbors.append(nNode)
            if nNode.SLACode == self.SLACode and nNode.SLACode != 0:
                self.mySLANeighbors.append(nNode)
            elif nNode.SLACode != 0:    self.SLANeighbors.append(nNode)
            else:                       self.NonSLANeighbors.append(nNode)