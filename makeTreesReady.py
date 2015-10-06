import sys
from subprocess import call
from datetime import date
import os
import ROOT
import glob

# changed to handle new analyzer where JES trees are doen with the same scripts

if len(sys.argv)<=2:
  print "script to manage the BoostedAnalyzer output trees"
  print "open every file in the given JobList.txt and reads its contents"
  print "it will check if they have a minimal filesize and will hadd them together or rewrite the given JobList.txt"
  print "sample combination depends on the direcotries the trees are in"
  print "will also merge the cutflows, copy the folder with the JobScripts and create the Yield Tables"
  print "usage:"
  print "python makeTreesReady.py [-j] UTPUT_DIRECTORY JOBLIST.TXT "
  print "-j  also handle JES/JER trees if they dont have their own JobScripts"
  exit(0)

DONEWJESVARIATION=False
if sys.argv[1]=="-j":
  DONEWJESVARIATION=True
  outPath = sys.argv[2]
  sampleList=sys.argv[3]
else :
  outPath = sys.argv[1]
  sampleList=sys.argv[2]

checklogs=False

print "Path to skimmed Samples ", outPath

sampleListFile=open(sampleList,"r")
jobFiles=list(sampleListFile)
#print jobFiles

call(["mkdir",outPath+"/addedTrees"])
call(["mkdir",outPath+"/addedTrees/AnalysisConfigs"])
log=open(outPath+"/addedTrees/AnalysisConfigs/AnalysisLog.txt","w")

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
        if DONEWJESVARIATION:
          s.append(outSampleFile.replace("nominal","JESUP"))
          s.append(outSampleFile.replace("nominal","JESDOWN"))
          s.append(outSampleFile.replace("nominal","JERUP"))
          s.append(outSampleFile.replace("nominal","JERDOWN"))
  if sampleAlreadyExists==False:
    if DONEWJESVARIATION:
      sampleFiles.append([outSamplePath,outSampleFile,outSampleFile.replace("nominal","JESUP"),outSampleFile.replace("nominal","JESDOWN"),outSampleFile.replace("nominal","JERUP"),outSampleFile.replace("nominal","JERDOWN")])
    else:
      sampleFiles.append([outSamplePath,outSampleFile])
  filef.close()

#print samples
#print "individual files:"
print sampleFiles
#exit(0)


sampleListFile.close()

log.write("Path to Samples "+outPath+"\n")
log.write("produced on "+str(date.today())+"\n\n")
log.write("Samples and theirs SubSamples\n\n")
for s in samples:
  log.write(s[0]+"\n")
  for ss in s[1:]:
    log.write(ss+"\n")
  log.write("\n")

#copy the scripts to make the the trees and the sampleList.txt to the output folder
call(["cp","-r","output",outPath+"/addedTrees/JObScripts"])
print "copied the job scripts"

call(["cp",sampleList,sampleList+"_original"])
# check each file for size and existence
everythingAllright=True
newSampleListFile=open("output/sampleListe_Problems.txt","w")
ROOT.gErrorIgnoreLevel=ROOT.kError
JobsToRedo=[]
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
        if l.find(f)>=0 or l.find(f.replace("JESUP","nominal"))>=0 or l.find(f.replace("JESDOWN","nominal"))>=0 or l.find(f.replace("JERUP","nominal"))>=0 or l.find(f.replace("JERDOWN","nominal"))>=0:
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
    print size>100 , sizecutflow>1 , ffexists , cffexists , treeIsGood , InitialEventsFromCutflow==nEventsFromInputFiles , FinalEventsFromCutflow==nEventsFromOutputTree , logFileIsGood
    print InitialEventsFromCutflow, nEventsFromInputFiles , FinalEventsFromCutflow, nEventsFromOutputTree 


    if thisJobisOK==False:
      print "something wrong with "+ff
      everythingAllright=False 
      print "corresponing job file :"+thisJobFile
      if thisJobFile not in JobsToRedo:
        JobsToRedo.append(thisJobFile)
    print JobsToRedo

for j in JobsToRedo:
  newSampleListFile.write(j+"\n")
newSampleListFile.close()

if everythingAllright==False:
  print "rewrote sampleList.txt -> Ready to do runProblems.sh"
  exit(0)

if everythingAllright==True:
  print "all files seem to be ok -> adding trees"

log.write("hadded Trees and merged Cutflows\n\n")
AllCutflows_nominal=[]
AllCutflows_JESUP=[]
AllCutflows_JESDOWN=[]
MergedCutflows_JESUP=[]
MergedCutflows_JESDOWN=[]
AllCutflows_JERUP=[]
AllCutflows_JERDOWN=[]
MergedCutflows_JERUP=[]
MergedCutflows_JERDOWN=[]
MergedCutflows_nominal=[]
print sampleFiles
for s in sampleFiles:
  name=s[0].rsplit("/",1)[1]
  addedPath=s[0].rsplit("/",1)[0]
  trees_nominal=[]
  trees_JESUP=[]
  trees_JESDOWN=[]
  trees_JERUP=[]
  trees_JERDOWN=[]
  cutflows_nominal=[]
  cutflows_JESUP=[]
  cutflows_JESDOWN=[]
  cutflows_JERUP=[]
  cutflows_JERDOWN=[]
  subSamplecutflows_nominal=[]
  subSamplecutflows_JESUP=[]
  subSamplecutflows_JESDOWN=[]
  subSamplecutflows_JERUP=[]
  subSamplecutflows_JERDOWN=[]
  subSamples=[]

  for f in s[1:]:
    ff = f+"_Tree.root"
    if ff.find("nominal")>=0:
      trees_nominal.append(ff)
    if ff.find("JESUP")>=0:
      trees_JESUP.append(ff)
    if ff.find("JESDOWN")>=0:
      trees_JESDOWN.append(ff)
    if ff.find("JERUP")>=0:
      trees_JERUP.append(ff)
    if ff.find("JERDOWN")>=0:
      trees_JERDOWN.append(ff)
    cff=f+"_Cutflow.txt"
    sf=f.rsplit("_",1)[0]
    #print sf 
    if sf not in subSamples:
      subSamples.append(sf)
      if cff.find("nominal")>=0:
        subSamplecutflows_nominal.append([sf])
      if cff.find("JESUP")>=0:      
        subSamplecutflows_JESUP.append([sf])
      if cff.find("JESDOWN")>=0:      
        subSamplecutflows_JESDOWN.append([sf])
      if cff.find("JERUP")>=0:      
        subSamplecutflows_JERUP.append([sf])
      if cff.find("JERDOWN")>=0:      
        subSamplecutflows_JERDOWN.append([sf])
    #print "subsamples", subSamples, "\n"
    #print "subsample cutflows", subSamplecutflows_nominal, "\n"
    if cff.find("nominal")>=0:
      cutflows_nominal.append(cff)
      for subsample in subSamplecutflows_nominal:
        if sf==subsample[0]:
          subsample.append(cff)
    if cff.find("JESUP")>=0:
      cutflows_JESUP.append(cff)
      for subsample in subSamplecutflows_JESUP:
        if sf==subsample[0]:
          subsample.append(cff)
    if cff.find("JESDOWN")>=0:
      cutflows_JESDOWN.append(cff)
      for subsample in subSamplecutflows_JESDOWN:
        if sf==subsample[0]:
          subsample.append(cff)
    if cff.find("JERUP")>=0:
      cutflows_JERUP.append(cff)
      for subsample in subSamplecutflows_JERUP:
        if sf==subsample[0]:
          subsample.append(cff)
    if cff.find("JERDOWN")>=0:
      cutflows_JERDOWN.append(cff)
      for subsample in subSamplecutflows_JERDOWN:
        if sf==subsample[0]:
          subsample.append(cff)

  if len(trees_nominal)>0:
    an=addedPath+"/addedTrees/"+name+"_nominal.root"
    mn=addedPath+"/addedTrees/"+name+"_nominal_Cutflow.txt"
    call(["rm","-f",an])
    call(["hadd",an]+trees_nominal)
    call(["python","merge_cutflow.py",mn]+cutflows_nominal)
    log.write(an+"\n")
    if len(subSamplecutflows_nominal)>1:
      for subsample in subSamplecutflows_nominal:
        ssn=subsample[0].rsplit("/",1)[1]
        #print ssn
        smn=addedPath+"/addedTrees/"+ssn+"_Cutflow.txt"
        sscf=subsample[1:]
        call(["python","merge_cutflow.py",smn]+sscf)
        log.write(smn+"\n")
        print "merged cutflows for ", smn
        AllCutflows_nominal.append(smn)
    else:
      AllCutflows_nominal.append(mn)
    MergedCutflows_nominal.append(mn)
    log.write(mn+"\n")
  if len(trees_JESUP)>0:
    an=addedPath+"/addedTrees/"+name+"_JESUP.root"
    mn=addedPath+"/addedTrees/"+name+"_JESUP_Cutflow.txt"
    call(["rm","-f",an])
    call(["hadd",an]+trees_JESUP)
    call(["python","merge_cutflow.py",mn]+cutflows_JESUP)
    log.write(an+"\n")
    if len(subSamplecutflows_JESUP)>1:
      for subsample in subSamplecutflows_JESUP:
        ssn=subsample[0].rsplit("/",1)[1]
        #print ssn
        smn=addedPath+"/addedTrees/"+ssn+"_Cutflow.txt"
        call(["python","merge_cutflow.py",smn]+subsample[1:])
        log.write(smn+"\n")
        AllCutflows_JESUP.append(smn)
    else:
      AllCutflows_JESUP.append(mn)
    MergedCutflows_JESUP.append(mn)
    log.write(mn+"\n")

  if len(trees_JESDOWN)>0:
    an=addedPath+"/addedTrees/"+name+"_JESDOWN.root"
    mn=addedPath+"/addedTrees/"+name+"_JESDOWN_Cutflow.txt"
    call(["rm","-f",an])
    call(["hadd",an]+trees_JESDOWN)
    call(["python","merge_cutflow.py",mn]+cutflows_JESDOWN)
    log.write(an+"\n")
    if len(subSamplecutflows_JESDOWN)>1:
      for subsample in subSamplecutflows_JESDOWN:
        ssn=subsample[0].rsplit("/",1)[1]
        #print ssn
        smn=addedPath+"/addedTrees/"+ssn+"_Cutflow.txt"
        call(["python","merge_cutflow.py",smn]+subsample[1:])
        log.write(smn+"\n")
        AllCutflows_JESDOWN.append(smn)
    else:
      AllCutflows_JESDOWN.append(mn)
    MergedCutflows_JESDOWN.append(mn)
    log.write(mn+"\n")

  if len(trees_JERUP)>0:
    an=addedPath+"/addedTrees/"+name+"_JERUP.root"
    mn=addedPath+"/addedTrees/"+name+"_JERUP_Cutflow.txt"
    call(["rm","-f",an])
    call(["hadd",an]+trees_JERUP)
    call(["python","merge_cutflow.py",mn]+cutflows_JERUP)
    log.write(an+"\n")
    if len(subSamplecutflows_JERUP)>1:
      for subsample in subSamplecutflows_JERUP:
        ssn=subsample[0].rsplit("/",1)[1]
        #print ssn
        smn=addedPath+"/addedTrees/"+ssn+"_Cutflow.txt"
        call(["python","merge_cutflow.py",smn]+subsample[1:])
        log.write(smn+"\n")
        AllCutflows_JERUP.append(smn)
    else:
      AllCutflows_JERUP.append(mn)
    MergedCutflows_JERUP.append(mn)
    log.write(mn+"\n")

  if len(trees_JERDOWN)>0:
    an=addedPath+"/addedTrees/"+name+"_JERDOWN.root"
    mn=addedPath+"/addedTrees/"+name+"_JERDOWN_Cutflow.txt"
    call(["rm","-f",an])
    call(["hadd",an]+trees_JERDOWN)
    call(["python","merge_cutflow.py",mn]+cutflows_JERDOWN)
    log.write(an+"\n")
    if len(subSamplecutflows_JERDOWN)>1:
      for subsample in subSamplecutflows_JERDOWN:
        ssn=subsample[0].rsplit("/",1)[1]
        #print ssn
        smn=addedPath+"/addedTrees/"+ssn+"_Cutflow.txt"
        call(["python","merge_cutflow.py",smn]+subsample[1:])
        log.write(smn+"\n")
        AllCutflows_JERDOWN.append(smn)
    else:
      AllCutflows_JERDOWN.append(mn)
    MergedCutflows_JERDOWN.append(mn)
    log.write(mn+"\n")

  log.write("\n")
print "added trees and merged the cutflows"

yieldpaths=outPath+"/addedTrees/CutflowTables/"
call(["mkdir",yieldpaths])
# doint the yield tables
if len(AllCutflows_nominal)>0:
  on=yieldpaths+"SubSamples_nominal"
  call(["python","makeCutflowTables.py",on]+AllCutflows_nominal)
if len(AllCutflows_JESUP)>0:
  on=yieldpaths+"SubSamples_JESUP"
  call(["python","makeCutflowTables.py",on]+AllCutflows_JESUP)
if len(AllCutflows_JESDOWN)>0:
  on=yieldpaths+"SubSamples_JESDOWN"
  call(["python","makeCutflowTables.py",on]+AllCutflows_JESDOWN)
if len(AllCutflows_JERUP)>0:
  on=yieldpaths+"SubSamples_JERUP"
  call(["python","makeCutflowTables.py",on]+AllCutflows_JERUP)
if len(AllCutflows_JERDOWN)>0:
  on=yieldpaths+"SubSamples_JERDOWN"
  call(["python","makeCutflowTables.py",on]+AllCutflows_JERDOWN)


if len(MergedCutflows_nominal)>0:
  on=yieldpaths+"Merged_nominal"
  call(["python","makeCutflowTables.py",on]+MergedCutflows_nominal)
if len(MergedCutflows_JESUP)>0:
  on=yieldpaths+"Merged_JESUP"
  call(["python","makeCutflowTables.py",on]+MergedCutflows_JESUP)
if len(MergedCutflows_JESDOWN)>0:
  on=yieldpaths+"Merged_JESDOWN"
  call(["python","makeCutflowTables.py",on]+MergedCutflows_JESDOWN)
if len(MergedCutflows_JERUP)>0:
  on=yieldpaths+"Merged_JERUP"
  call(["python","makeCutflowTables.py",on]+MergedCutflows_JERUP)
if len(MergedCutflows_JERDOWN)>0:
  on=yieldpaths+"Merged_JERDOWN"
  call(["python","makeCutflowTables.py",on]+MergedCutflows_JERDOWN)
log.close()

#finally collect BoostedTTH and MiniAODHelper Software and put them in a tarball
call(["tar","-a","-cf",outPath+"/addedTrees/AnalysisConfigs/CMSSW.tar.gz","/afs/desy.de/user/k/kelmorab/CMSSW_7_2_3/src/BoostedTTH","/afs/desy.de/user/k/kelmorab/CMSSW_7_2_3/src/MiniAOD"])
call(["tar","-a","-cf",outPath+"/addedTrees/AnalysisConfigs/runscripts.tar.gz","/afs/desy.de/user/k/kelmorab/runNew"])
print "created tarball with used software"




