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
indirs=sys.argv[2:]
name = sys.argv[1]
if not name.startswith("--name="):
    print("first argument should be --name=NAME of output files")
    print("as this is not the case, no additional name will be given")
    indirs += sys.argv[1]
    name = ""
else:
    name = name[7:]+"_"


fileList=[]
for dir in indirs:
    if "*" in dir:
        fileList+=glob.glob(dir)
    else:
        fileList+=glob.glob(dir+"/*.root")


print("number of files: {}".format(len(fileList)))
for i, fil in enumerate(fileList):
    if i%100==0: print("\n\033[1;31m{}\033[0m\n".format("checking file {}/{}".format(i, len(fileList))))
    status = checkROOTFiles(fil)
    if status=="broken":
        brokenFiles.append(fil) 
    if status=="empty":
        emptyFiles.append(fil)

with open(name+"broken_files.txt", "w") as f:
    f.write("\n".join(brokenFiles))
with open(name+"empty_files.txt", "w") as f:
    f.write("\n".join(emptyFiles))

print("\033[1;31m{}\033[0m".format("number of files: {}".format(len(fileList))))
print("\033[1;31m{}\033[0m".format("files broken: {}".format(len(brokenFiles))))
print("\033[1;31m{}\033[0m".format("files empty: {}".format(len(emptyFiles))))
