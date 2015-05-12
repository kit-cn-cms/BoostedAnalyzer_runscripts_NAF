import sys
from subprocess import call
from datetime import date

if len(sys.argv)<=2:
  print "script to manage the BoostedAnalyzer output trees"
  print "open every file in the given JobList.txt and reads its contents"
  print "it will check if they have a minimal filesize and will hadd them together or rewrite the given JobList.txt"
  print "sample combination depends on the direcotries the trees are in"
  print "will also merge the cutflows, copy the folder with the JobScripts and create the Yield Tables"
  print "usage:"
  print "python makeTreesReady.py JOBLIST.TXT OUTPUT_DIRECTORY"
  exit(0)

outPath = sys.argv[1]
sampleList=sys.argv[2]

print "Path to skimmed Samples ", outPath

sampleListFile=open(sampleList,"r")
jobFiles=list(sampleListFile)
print jobFiles
log=open(outPath+"/addedTrees/AnalysisLog.txt","w")

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

log.write("Path to Samples "+outPath+"\n")
log.write("produced on "+str(date.today())+"\n\n")
log.write("Samples and theirs SubSamples\n\n")
for s in samples:
  log.write(s[0]+"\n")
  for ss in s[1:]:
    log.write(ss+"\n")
  log.write("\n")

#copy the scripts to make the the trees and the sampleList.txt to the output folder
call(["cp","-r","output",outPath+"/addedTrees/"])
print "copied the job scripts"

call(["cp",sampleList,sampleList+"_original"])
# check each file for size and existence
everythingAllright=True
newSampleListFile=open("output/sampleListe_Problems.txt","w")
for s in sampleFiles:
  #print s[0]
  for f in s[1:]:
    #print f
    tmpfile=open("tmp.txt","w")
    ff = f+"_Tree.root"
    call(["du",ff],stdout=tmpfile,stderr=tmpfile)
    tmpfile.close()
    tmpfile=open("tmp.txt","r")
    bufferf=list(tmpfile)
    firstpart=bufferf[0].split("\t")[0]
    tmpfile.close()
    #print size
    size=0
    print firstpart
    if firstpart.find("cannot access")==-1:
      size=int(firstpart)
    if size<100:
      print "something wrong with "+ff
      everythingAllright=False 
      for job in jobFiles:
        filename=job.rsplit("\n",1)[0]
        filef=open(filename,"r")
        lines=list(filef)
        #print lines
        #print f
        for l in lines:
          if l.find(f)>=0:
            print "corresponing job file :"+filename
            newSampleListFile.write(filename+"\n")
        filef.close()
newSampleListFile.close()

if everythingAllright==False:
  print "rewrote sampleList.txt -> Ready to do runProblems.sh"
  exit(0)

if everythingAllright==True:
  print "all files seem to be ok -> adding trees"

log.write("hadded Trees and merged Cutflows\n\n")
AllCutflows_nominal=[]
AllCutflows_JESUP=[]
AllCutflows_JEDOWN=[]
MergedCutflows_JESUP=[]
MergedCutflows_JESDOWN=[]
MergedCutflows_nominal=[]
for s in sampleFiles:
  name=s[0].rsplit("/",1)[1]
  addedPath=s[0].rsplit("/",1)[0]
  trees_nominal=[]
  trees_JESUP=[]
  trees_JESDOWN=[]
  cutflows_nominal=[]
  cutflows_JESUP=[]
  cutflows_JESDOWN=[]
  subSamplecutflows_nominal=[]
  subSamplecutflows_JESUP=[]
  subSamplecutflows_JESDOWN=[]
  subSamples=[]
  AllCutflows_nominal=[]
  AllCutflows_JESUP=[]
  AllCutflows_JEDOWN=[]
  MergedCutflows_JESUP=[]
  MergedCutflows_JESDOWN=[]
  MergedCutflows_nominal=[]

  for f in s[1:]:
    ff = f+"_Tree.root"
    if ff.find("nominal")>=0:
      trees_nominal.append(ff)
    if ff.find("JESUP")>=0:
      trees_JESUP.append(ff)
    if ff.find("JESDOWN")>=0:
      trees_JEDOWN.append(ff)
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
      cutflows_JEDOWN.append(cff)
      for subsample in subSamplecutflows_JESDOWN:
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
  log.write("\n")
print "added trees and merged the cutflows"

# doint the yield tables
if len(AllCutflows_nominal)>0:
  on=addedPath+"/addedTrees/SubSamples_nominal"
  call(["python","makeYieldTables.py",on]+AllCutflows_nominal)
if len(AllCutflows_JESUP)>0:
  on=addedPath+"/addedTrees/SubSamples_JESUP"
  call(["python","makeYieldTables.py",on]+AllCutflows_JESUP)
if len(AllCutflows_JESDOWN)>0:
  on=addedPath+"/addedTrees/SubSamples_JESDOWN"
  call(["python","makeYieldTables.py",on]+AllCutflows_JESDOWN)

if len(MergedCutflows_nominal)>0:
  on=addedPath+"/addedTrees/Merged_nominal"
  call(["python","makeYieldTables.py",on]+MergedCutflows_nominal)
if len(MergedCutflows_JESUP)>0:
  on=addedPath+"/addedTrees/Merged_JESUP"
  call(["python","makeYieldTables.py",on]+MergedCutflows_JESUP)
if len(MergedCutflows_JESDOWN)>0:
  on=addedPath+"/addedTrees/Merged_JESDOWN"
  call(["python","makeYieldTables.py",on]+MergedCutflows_JESDOWN)

log.close()





