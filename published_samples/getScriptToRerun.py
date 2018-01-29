import sys
import os
import glob
import ROOT
import subprocess
import xml.etree.ElementTree as ET

removeRecovered=False
deleteTheNTuples=False
deleteTheEMPTYNTuples=False
ignoreQstat=True

def checkROOTFiles(path=""):
  isGOOD=True
  rf=ROOT.TFile.Open(path)
  if rf==None or len(rf.GetListOfKeys())==0 or rf.TestBit(ROOT.TFile.kZombie):
    isGOOD=False
    print "BROKEN    ", path
  elif removeRecovered and rf.TestBit(ROOT.TFile.kRecovered):
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
	isGOOD="EMPTY"
	print "EMPTY    ", path
  if rf!=None:
    rf.Close()
  return isGOOD


#prefix=sys.argv[1
arguments=sys.argv[1:]
if len(arguments)==0 or "-h" in arguments or not "-d" in arguments:
  print "usage"
  print "python getScriptToRerun.py [--removeRecovered] [--delete] -d LOGPATH [-v VETOLIST]"
  print "--removeRecovered: Also flag those jobs as problematic of the keys of the root files could be recovered"
  print "--delete: Actually delete the root files that belong to the problematic jobs"
  print "-d LOGPATH: Path to log files to be analyzed"
  print "-v VETOLIST: these log files are ignored. Use a space separated list here. e.g. -v file1,file2,file3"

indir=""
vetolist=[]
for iarg,arg in enumerate(arguments):
  if "--removeRecovered"==arg:
    removeRecovered=True
  if "--removeEmpty"==arg:
    deleteTheEMPTYNTuples=True
  if "--delete"==arg:
    deleteTheNTuples=True
  if "-d"==arg:
    indir=arguments[iarg+1]
  if "-v"==arg:
    vetolist=arguments[iarg+1].split(",")

infiles=glob.glob(indir+"/*.o*")
undoneList=[]
doneList=[]
qstatjobslist=[]
ListOfAllEmptyTrees=[]
tempfile=open("tempqstatfile.txt","w")
cmd="qstat -xml"
subprocess.call([cmd],shell=True,stdout=tempfile)
tempfile.close()
tree=ET.parse("tempqstatfile.txt")
root=tree.getroot()
for j in root[0]:
  #print j[0].text
  qstatjobslist.append(j[2].text)
#print qstatjobslist
#exit(0)
ntuplesToDelete=[]

for fi in infiles:
  ignoreJob=False
  for v in vetolist:
    if v in fi:
      ignoreJob=True
  if ignoreJob:
    print "ignoring (perhaps still running): ", fi
    continue
  propername=fi.replace(indir+"/","").split(".o")[0]
  if propername in qstatjobslist and ignoreQstat==False:
    print "job ist still running ", propername
    continue
  
  # If the jobs are not still running we check the log files for several things
  # check stdout file 
  ifi=open(fi,"r")
  ifl=list(ifi)
  ntupleNames=[]
  treeWasWritten=False
  diskQuotaProblem=False
  segmentationViolation=False
  for l in reversed(ifl): 
    if "Tree Written" in l:
      treeWasWritten=True
      #break
    if "creating tree writer" in l:
      ntupleNames.append(l.rsplit(" ")[-1].replace("\n","")+"_Tree.root")
  propername=fi.replace(indir+"/","").split(".o")[0]
  ifi.close()
  # now check the corresponding error file
  errorfilename=fi.replace(".o",".e")
  efi=open(errorfilename,"r")
  efl=list(efi)
  for l in reversed(efl):
    if "Disk quota exceeded" in l:
      diskQuotaProblem=True
    if "egmentation" in l:
      segmentationViolation=True      
  efi.close()
  anyProblem = diskQuotaProblem or segmentationViolation
  if treeWasWritten==False or anyProblem==True:
    undoneList.append(propername)
    ntuplesToDelete+=ntupleNames
    print "PROBLEM WITH JOB ", propername
  
  # now we check whether there are problems with the root files themselves
  allNTuplesAreGood=True
  allNTuplesAreEmpty=False
  problematicTrees=[]
  emptyTrees=[]
  #print ntupleNames
  if treeWasWritten==True and anyProblem==False:
    for ntf in ntupleNames:
      if checkROOTFiles(ntf)==False:
	allNTuplesAreGood=False
        problematicTrees+=ntupleNames
        break
      elif checkROOTFiles(ntf)=="EMPTY":
	emptyTrees.append(ntf)
    if allNTuplesAreGood==False:
      undoneList.append(propername)
      ntuplesToDelete+=problematicTrees
      print "PROBLEM WITH FILE in job ", propername
  if deleteTheEMPTYNTuples==True:
    ntuplesToDelete+=emptyTrees
  if deleteTheNTuples:
    for ntf in ntuplesToDelete:
      if os.path.exists(ntf):
        os.remove(ntf) 
    ntuplesToDelete=[]
  if len(emptyTrees)!=0:
    ListOfAllEmptyTrees+=emptyTrees
  # this job seems to have worked
  if allNTuplesAreGood:
    doneList.append(propername)

print "the following ntuples were unproblematic but are empty"
print " ".join(ListOfAllEmptyTrees)
print ""
print "jobs to repeat"
print len(undoneList)
print " ".join(undoneList)
print ""
print ""
print "ntuples to delete"
print " ".join(ntuplesToDelete)

