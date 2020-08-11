from __future__ import print_function
import ROOT
import sys
import glob
from multiprocessing import Pool
ROOT.ROOT.EnableThreadSafety()


def checkROOTFile(path=""):
    isGOOD = True
    rf = ROOT.TFile.Open(path)
    if rf == None or len(rf.GetListOfKeys()) == 0 or rf.TestBit(ROOT.TFile.kZombie):
        isGOOD = False
        print ("BROKEN    ", path)
    elif rf.TestBit(ROOT.TFile.kRecovered):
        isGOOD = False
        print ("BROKEN    ", path)
    else:
        tree = rf.Get("MVATree")
        if tree == None:
            isGOOD = False
            print ("BROKEN    ", path)
        else:
            nevents = tree.GetEntries()
            rf.Close()
            if nevents < 0:
                isGOOD = False
                print ("BROKEN    ", path)
    if rf != None:
        rf.Close()
    return isGOOD


def checkROOTFiles(fileList):
    for fil in fileList:
        if not checkROOTFile(fil):
            brokenFiles.append(fil)
            print ("BROKEN    ", fil)
        else:
            print ("GOOD  ", fil)
    return brokenFiles


brokenFiles = []
nthreads = int(sys.argv[1])
indirs = sys.argv[2:]


fileList = []
for dir in indirs:
    if "*" in dir:
        fileList += glob.glob(dir)
    else:
        fileList += glob.glob(dir + "/*.root")

# split filelist into chuncks
chunks = [
    fileList[x : x + (len(fileList) / nthreads)]
    for x in xrange(0, len(fileList), len(fileList) / nthreads)
]
#print (chunks)
print("splitted into ", len(chunks), " chunks")

# spawn processes to check chunks
pool=Pool(processes=len(chunks))
print("spawned ", len(chunks), " processes")
brokenFiles = pool.map(checkROOTFiles,chunks)
pool.close()
pool.join()

# print broken files
print ("\n\n\n\n")
print ("to delete\n")
output_string = ""
for subFileList in brokenFiles:
    for File in subFileList:
        output_string+=" "+File
