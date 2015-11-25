#!/usr/bin/env python
# checks if the jobs corresponding to a list scripts finished successful
# usage: ./check_jobs.py joblist.txt
import os
import sys
import datetime
from subprocess import call

def parse(line):
    argument =line.split(' : ')[1]
    if argument.endswith('\n'): argument=argument[:-1]
    return argument

def events_from_cutflow(cutflow):
    if not os.path.exists(cutflow): return -1
    f=open(cutflow, 'r')
    line = f.readline().split(' : ')
    assert line[1]=='all'
    return line[2]
    f.close()

def check_job(j):
    nevents=-1
    cutflow=''
    check=[]
    jobfile=open(j,'r')
    for line in jobfile:
        if not line.startswith('#meta'): continue
        if 'nevents' in line:
            nevents=parse(line)
        if 'cutflow' in line:
            cutflow=parse(line)
        if 'check' in line:
            check.append(parse(line))
    files_ok=True
    missing_files=[]
    for c in check:
        if not os.path.exists(c): 
            files_ok=False
            missing_files.append(c)
    nevents2=events_from_cutflow(cutflow)
    if not files_ok and nevents!=nevents2 and nevents>0 and nevents2>0:
        return j+": files missing and wrong number of events, missing files: "+(",".join(missing_files))+", nevents == "+str(nevents)+"!="+str(nevents2)+" == nevents in cutflow"
    if files_ok and nevents!=nevents2:
        return j+": wrong number of events, nevents == "+str(nevents)+"!="+str(nevents2)+" == nevents in cutflow"
    if not files_ok and nevents==nevents2:
        return j+": files missing: "+",".join(missing_files)
    
logfile= sys.argv[1]
print 'the following jobs didnt finish successfully'
print 'note: if only the number of events is wrong this could be due to a filtering step that is not documented in the cutflow'
f_list=open(logfile,'r')
failed_jobs=[]
for line in f_list:
    if line.endswith('\n'): line=line[:-1]
    check=check_job(line)
    if check!=None:
        failed_jobs.append(line)
        print check
print "please resubmit"
print " ".join(failed_jobs)
if len(failed_jobs)==0:
    print 'all jobs finished successfully!'
