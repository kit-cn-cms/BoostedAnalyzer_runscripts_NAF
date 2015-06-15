import sys
from subprocess import call
from datetime import date
import os
import ROOT
import glob

if len(sys.argv)<=1:
  print "script to check the output files"
  print "open every file in the given JobList.txt and reads its contents"
  print "checks the output of the job"
  print "usage:"
  print "python CheckJobIntegrity.py [ -l ] JOBLIST.TXT "
  print "-l  will also check the logfiles of the jobs. Will lead to problems if there are old logfiles in the folder"
  exit(0)

checklogs=False
for arg in sys.argv:
  if arg=="-l":
   checklogs=True
  else:
    sampleList=arg

sampleListFile=open(sampleList,"r")
jobFiles=list(sampleListFile)

samples=[]
sampleFiles=[]

for job in jobFiles:
  #print job
  filename=job.rsplit("\n",1)[0]
  #print repr(filename)
  filef=open(filename,"r")
  lines=list(filef)
  #print lines
  for line in lines:
    if "FILE_NAMES" in line:
      bufferf=line.split("\"",1)[1]
      bufferf=bufferf.rsplit("\"",1)[0]
      bufferf=bufferf.split(" ")[0]
      rawSamplePath=bufferf.rsplit("/",1)[0]
      #print rawSamplePath
    if "OUTFILE_NAME" in line:
      bufferf=line.split("\"",1)[1]
      bufferf=bufferf.rsplit("\"",1)[0]
      outSamplePath=bufferf.rsplit("/",1)[0]
      outSampleFile=bufferf
      #print outSamplePath

  sampleAlreadyExists=False
  for s in samples:
    if outSamplePath==s[0]:
      sampleAlreadyExists=True
      if rawSamplePath not in s:
        s.append(rawSamplePath)
  if sampleAlreadyExists==False:
    samples.append([outSamplePath,rawSamplePath])

  sampleAlreadyExists=False
  for s in sampleFiles:
    if outSamplePath==s[0]:
      sampleAlreadyExists=True
      if outSampleFile not in s:
        s.append(outSampleFile)
  if sampleAlreadyExists==False:
    sampleFiles.append([outSamplePath,outSampleFile])
  filef.close()

#print samples
#print "individual files:"
#print sampleFiles
#exit(0)

sampleListFile.close()


# check each file for size and existence
everythingAllright=True
newSampleListFile=open("output/sampleListe_Problems.txt","w")
ROOT.gErrorIgnoreLevel=ROOT.kError
for s in sampleFiles:
  #print s[0]
  for f in s[1:]:
    thisJobisOK=False
    thisJobFile="NOTFOUND"
    InitialEventsFromCutflow=-1
    FinalEventsFromCutflow=-1
    nEventsFromInputFiles=0
    nEventsFromOutputTree=0
    size=0
    sizecutflow=0
    ffexists=False
    cffexists=False
    treeIsGood=False
    logFilehasTreeWritten=False
    logFileIsGood=True
 
    thisJobInputFiles=[]
    tmpfile=open("tmp.txt","w")
    ff = f+"_Tree.root"
    print "checking ", ff
    cff=ff.replace("Tree.root","Cutflow.txt")
    call(["du",ff],stdout=tmpfile,stderr=tmpfile)
    tmpfile.close()
    tmpfile=open("tmp.txt","r")
    bufferf=list(tmpfile)
    firstpart=bufferf[0].split("\t")[0]
    tmpfile.close()
    if firstpart.find("cannot access")==-1:
      size=int(firstpart)
    tmpfile=open("tmp.txt","w")
    call(["du",cff],stdout=tmpfile,stderr=tmpfile)
    tmpfile.close()
    tmpfile=open("tmp.txt","r")
    bufferf=list(tmpfile)
    firstpart=bufferf[0].split("\t")[0]
    tmpfile.close()
    if firstpart.find("cannot access")==-1:
      sizecutflow=int(firstpart)
    
# check existence and get number of events from cutflow and output tree
    ffexists=os.path.exists(ff)
    cffexists=os.path.exists(cff)
    if cffexists and sizecutflow>1:
      thisCutflowFile=open(cff,"r")
      cfflines=list(thisCutflowFile)
      for cffline in cfflines:
        if "all" in cffline:
          InitialEventsFromCutflow=int(cffline.replace(" ","").split(":")[2])
      FinalEventsFromCutflow=int(cfflines[len(cfflines)-1].replace(" ","").split(":")[2])
    #print InitialEventsFromCutflow, FinalEventsFromCutflow

    ftf=ROOT.TFile(ff,"READ")
    ftree=ftf.Get("MVATree")
    if ftree!=None:
      nEventsFromOutputTree=ftree.GetEntries()
      treeIsGood=True
    ftf.Close()
    #print nEventsFromOutputTree
#find jobfile corresponding to output tree
    for job in jobFiles:
      foundjobfile=False
      filename=job.rsplit("\n",1)[0]
      filef=open(filename,"r")
      lines=list(filef)
      for l in lines:
        if l.find(f)>=0:
          print "corresponing job file : "+filename
          thisJobFile=filename
          for ll in lines:
            if "FILE_NAMES" in ll:
              bufferf=ll.split("\"",1)[1]
              bufferf=bufferf.rsplit("\"",1)[0]
              thisJobInputFiles=bufferf.split(" ")
          #print thisJobInputFiles
          foundjobfile=True
          break
      filef.close()
      if foundjobfile:
        break
#get total number of input events from input trees
    for thisinfile in thisJobInputFiles:
      #print thisinfile
      if thisinfile=="" or thisinfile==" ":
        continue
      tf=ROOT.TFile(thisinfile,"READ")
      tree=tf.Get("Events") 
      nEventsFromInputFiles+=tree.GetEntries()
      tf.Close()
    #print nEventsFromInputFiles
# check the logfiles
# might want to not do this in case people dont delete the old logfiles first
    if checklogs:
      logFiles=glob.glob(thisJobFile.replace("output","logs").replace(".sh","")+".*")
      #print logFiles
      for logf in logFiles:
        thisLogFile=open(logf,"r")
        thisLogFileLines=list(thisLogFile)
        for thisLogFileline in thisLogFileLines:
          if "Tree Written" in thisLogFileline:
            logFilehasTreeWritten=True     
      logFileIsGood=logFilehasTreeWritten

    thisJobisOK = size>100 and sizecutflow>1 and ffexists and cffexists and treeIsGood and InitialEventsFromCutflow==nEventsFromInputFiles and FinalEventsFromCutflow==nEventsFromOutputTree and logFileIsGood
    #print size>100 , sizecutflow>1 , ffexists , cffexists , treeIsGood , InitialEventsFromCutflow==nEventsFromInputFiles , FinalEventsFromCutflow==nEventsFromOutputTree , logFileIsGood
    #print InitialEventsFromCutflow, nEventsFromInputFiles , FinalEventsFromCutflow, nEventsFromOutputTree 


    if thisJobisOK==False:
      print "something wrong with "+ff
      everythingAllright=False 
      print "corresponing job file :"+thisJobFile
      newSampleListFile.write(thisJobFile+"\n")
newSampleListFile.close()

if everythingAllright==False:
  print "rewrote sampleList.txt to output/sampleListe_Problems.txt -> Ready to do runProblems.sh"
  exit(0)

if everythingAllright==True:
  print "all files seem to be ok"
