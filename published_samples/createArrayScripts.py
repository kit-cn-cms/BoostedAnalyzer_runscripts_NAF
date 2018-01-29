#!/usr/bin/env python
# creates array scripts from *.sh files to cluster, either all scripts in a folder or just a list of files
# usage: ./createArrayScripts.py OUTPATH -f path/to/scripts [script_pattern]
# or ./createArrayScripts.py OUTPATH arbitrary number of filesnames

import glob
import sys
import stat
import os

nJobsPerArray=2000

pattern=''
path=''
files=[]
outpath=sys.argv[1]
if len(sys.argv) > 2 and sys.argv[2]=='-f':
    print "case 1"
    if len(sys.argv) > 3:
        path= sys.argv[3]+'/'
    if len(sys.argv) > 4:
        pattern= sys.argv[4]

    files = [os.path.join(root, name)
             for root, dirs, files in os.walk('./'+path)
             for name in files
             if pattern in name and name.endswith((".sh"))]

else:
    print "case 2"
    files=sys.argv[2:]

print len(files)

if not os.path.exists(outpath):
    os.makedirs(outpath)

nscripts=0
narrays=0

lol=[[]]
for f in files:
  lol[-1].append(f)
  nscripts+=1
  if nscripts >= nJobsPerArray:
    lol.append([])
    nscripts=0

logdir=os.getcwd()+"/logs"
if not os.path.exists(logdir):
    os.makedirs(logdir)
    
for scriptlist in lol:
  print len(scriptlist)
  # create an array script for each packet of 10000 jobs
  arrayscriptpath=outpath+"/ats_"+str(narrays)+".sh"
  arrayscriptcode="#!/bin/bash \n"
  arrayscriptcode+="#ARRAYMETA: ntasks "+str(len(scriptlist))+"\n"
  arrayscriptcode+="subtasklist=(\n"
  for scr in scriptlist:
    #print scr
    nl=os.getcwd()+"/"+scr+" \n"
    nl=nl.replace("/./","/")
    arrayscriptcode+=nl
  arrayscriptcode+=")\n"
  arrayscriptcode+="thescript=${subtasklist[$SGE_TASK_ID-1]}\n"
  arrayscriptcode+="thescriptbasename=`basename ${subtasklist[$SGE_TASK_ID-1]}`\n"
  arrayscriptcode+="echo \"${thescript}\n"
  arrayscriptcode+="echo \"${thescriptbasename}\n"
  arrayscriptcode+=". $thescript 1>>"+logdir+"/${thescriptbasename}.o$JOB_ID.$SGE_TASK_ID 2>>"+logdir+"/${thescriptbasename}.e$JOB_ID.$SGE_TASK_ID\n"
  arrayscriptfile=open(arrayscriptpath,"w")
  arrayscriptfile.write(arrayscriptcode)
  arrayscriptfile.close()
  st = os.stat(arrayscriptpath)
  os.chmod(arrayscriptpath, st.st_mode | stat.S_IEXEC)
  narrays+=1






























