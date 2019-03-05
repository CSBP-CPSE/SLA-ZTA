from math import cos, asin, sqrt

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin..


def leftMergeDictArray(array1, array2, var1, var2, keepAll = True):
     for a in range(0, len(array1)):
        found = False
        dic = array1[a]
        mvar1 = dic[var1]
        for b in range(0, len(array2)):
            dic2 = array2[b]
            mvar2 = dic2[var2]
            if mvar1 == mvar2:
                found = True
                lkeys = dic.keys()
                for k in dic2.keys():
                    k1 = k
                    if k in lkeys: k1 = k + "_2"
                    dic[k1] = dic2[k]
        if not found:
            dic2 = array2[0]
            lkeys = dic.keys()
            for k in dic2.keys():
                k1 = k
                if k in lkeys: k1 = k + "_2"
                dic[k1] = -1
     return array1


def outputDictArray(array, fname):
    filename = fname + '.csv'
    f = open(filename,'w')
    line = ""
    kArray = sorted(array[0].keys())
    for k in kArray:        line += k +","
    f.write(line +'\n')

    for a in range(0, len(array)):
        dic = array[a]
        line = ""
        for k in kArray:
            line += str(dic[k]) +","
        f.write(line)
        f.write('\n')
    f.close()

def outputCSDs(CSDDict, fname):
    filename = fname + '.csv'
    f = open(filename,'w')
    line = "CSD,CMA,isCMA,Population,OriginalCode,NewCode,Changed,ChangeType,Split"
    f.write(line +'\n')

    kArray = sorted(CSDDict.keys())
    for a in range(0, len(kArray)):
        code = kArray[a]
        CSD = CSDDict[code]
        line = ""
        line += str(CSD.CSDCode) +"," + str(CSD.CMACACode) +"," + str(CSD.CMACA) +"," + str(CSD.CSDPop) +"," + str(CSD.originalSLACode) + "," + str(CSD.SLACode) +"," + str(CSD.changed) +"," + str(CSD.changeType) +"," + str(CSD.split)
        f.write(line)
        f.write('\n')
    f.close()