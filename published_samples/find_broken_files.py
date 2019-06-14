import ROOT
import sys
import glob

def checkROOTFiles(path=""):
    isGOOD=True
    isEMPTY=False
    rf=ROOT.TFile.Open(path)
    if rf==None or len(rf.GetListOfKeys())==0 or rf.TestBit(ROOT.TFile.kZombie):
        isGOOD=False
        print "BROKEN        ", path
    elif rf.TestBit(ROOT.TFile.kRecovered):
        isGOOD=False
        print "BROKEN        ", path
    else:
        tree=rf.Get("MVATree")
        if tree==None:
            isGOOD=False
            print "BROKEN        ", path
        else:    
            nevents=tree.GetEntries()
            rf.Close()
            if nevents==0:
                isEMPTY=True
                print "EMTPY        ", path
            elif nevents<0:
                isGOOD=False
		print "BROKEN        ", path
    if rf!=None:
        rf.Close()
    if isEMPTY: return "empty"
    if isGOOD:  return "good"
    else:       return "broken"
    
    return isGOOD

brokenFiles=[]
emptyFiles=[]
indirs=sys.argv[1:]


fileList=[]
for dir in indirs:
    if "*" in dir:
        fileList+=glob.glob(dir)
    else:
        fileList+=glob.glob(dir+"/*.root")


print "number of files   ", len(fileList)
for fil in fileList:
    status = checkROOTFiles(fil)
    if status=="broken":
        brokenFiles.append(fil) 
    if status=="empty":
        emptyFiles.append(fil)

with open("broken_files.txt", "w") as f:
    f.write("\n".join(brokenFiles))
with open("empty_files.txt", "w") as f:
    f.write("\n".join(emptyFiles))
