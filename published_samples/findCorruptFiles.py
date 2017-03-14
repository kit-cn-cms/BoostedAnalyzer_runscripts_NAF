import ROOT
import sys
import glob

brokenFiles=[]
indirs=sys.argv[1:]

fileList=[]
for dir in indirs:
  fileList+=glob.glob(dir+"/*.root")

#print fileList
for fil in fileList:
  rf=ROOT.TFile.Open(fil)
  if rf==None or len(rf.GetListOfKeys())==0:
    brokenFiles.append(fil)
    print "BROKEN    ", fil
  else:
    tree=rf.Get("MVATree")
    nevents=tree.GetEntries()
    rf.Close()
    if nevents>0:  
      print "GOOD  ", fil
    else:
      brokenFiles.append(fil)
      print "BROKEN    ", fil


print ""
print ""
print ""
print ""
print "to delete"
print " ".join(brokenFiles)
