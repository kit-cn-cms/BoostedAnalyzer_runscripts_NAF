import ROOT
import sys
import glob

def checkROOTFiles(path=""):
  isGOOD=True
  rf=ROOT.TFile.Open(path)
  if rf==None or len(rf.GetListOfKeys())==0 or rf.TestBit(ROOT.TFile.kZombie):
    isGOOD=False
    print "BROKEN    ", path
  elif rf.TestBit(ROOT.TFile.kRecovered):
    isGOOD=False
    print "BROKEN    ", path
  else:
    tree=rf.Get("MVATree")
    if tree==None:
      isGOOD=False
      print "BROKEN    ", path
    else:  
      nevents=tree.GetEntries()
      rf.Close()
      if nevents<=0:
	isGOOD=False
	print "BROKEN    ", path
  if rf!=None:
    rf.Close()
  return isGOOD

brokenFiles=[]
indirs=sys.argv[1:]


fileList=[]
for dir in indirs:
  if "*" in dir:
    fileList+=glob.glob(dir)
  else:
    fileList+=glob.glob(dir+"/*.root")


#print fileList
for fil in fileList:
  if not checkROOTFiles(fil):
    brokenFiles.append(fil)
    print "BROKEN    ", fil
  else:
      print "GOOD  ", fil


print ""
print ""
print ""
print ""
print "to delete"
print " ".join(brokenFiles)
