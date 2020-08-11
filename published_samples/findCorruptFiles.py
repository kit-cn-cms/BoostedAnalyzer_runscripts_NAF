from __future__ import print_function
import ROOT
import sys
import glob


def checkROOTFiles(path="",treename_="MVATree"):
    isGOOD = True
    rf = ROOT.TFile.Open(path)
    if rf == None or len(rf.GetListOfKeys()) == 0 or rf.TestBit(ROOT.TFile.kZombie):
        isGOOD = False
        print ("BROKEN    ", path)
    elif rf.TestBit(ROOT.TFile.kRecovered):
        isGOOD = False
        print ("BROKEN    ", path)
    else:
        tree = rf.Get(treename_)
        if tree == None:
            isGOOD = False
            print ("BROKEN    ", path)
        else:
            nevents = tree.GetEntries()
            rf.Close()
            if nevents < 0:
                isGOOD = False
                print ("BROKEN    ", path)
            if nevents > 80000:
                isGOOD = False
                print ("TOO MANY EVENTS!!!", path)
    if rf != None:
        rf.Close()
    return isGOOD


brokenFiles = []
treename = sys.argv[1]
indirs = sys.argv[2:]


fileList = []
for dir in indirs:
    if "*" in dir:
        fileList += glob.glob(dir)
    else:
        fileList += glob.glob(dir + "/*.root")


# print fileList
for fil in fileList:
    if not checkROOTFiles(fil,treename):
        brokenFiles.append(fil)
        print ("BROKEN    ", fil)
    else:
        print ("GOOD  ", fil)


print ("")
print ("")
print ("")
print ("")
print ("to delete")
print (" ".join(brokenFiles))
