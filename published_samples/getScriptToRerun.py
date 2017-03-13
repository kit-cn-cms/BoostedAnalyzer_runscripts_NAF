import sys
import os
import glob
import subprocess
import xml.etree.ElementTree as ET

#prefix=sys.argv[1]
indir=sys.argv[1]
vetolist=sys.argv[2:]
infiles=glob.glob(indir+"/*.o*")
undoneList=[]
doneList=[]
qstatjobslist=[]
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

for fi in infiles:
  ignoreJob=False
  for v in vetolist:
    if v in fi:
      ignoreJob=True
  if ignoreJob:
    print "ignoring (perhaps still running): ", fi
    continue
  ifi=open(fi,"r")
  ifl=list(ifi)
  #print ifl
  treeWasWritten=False
  for l in reversed(ifl):
    if "Tree Written" in l:
      treeWasWritten=True
      break
  propername=fi.replace(indir+"/","").split(".o")[0]
  if treeWasWritten:
    doneList.append(propername)
  elif propername in qstatjobslist:
    print "job ist still running ", propername
  else:
    undoneList.append(propername)
    
print "jobs to repeat"
print len(undoneList)
print " ".join(undoneList)
