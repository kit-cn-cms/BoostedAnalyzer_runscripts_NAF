#!/usr/bin/env python
# submits alls *.sh files to cluster
# usage: ./sup.py path/to/scripts [script_pattern]
import os
import sys
from subprocess import call

pattern=''
path=''

if len(sys.argv) > 1:
    path= sys.argv[1]+'/'
if len(sys.argv) > 2:
    pattern= sys.argv[2]

if not os.path.exists('logs'):
    os.makedirs('logs')

files = [os.path.join(root, name)
                     for root, dirs, files in os.walk('./'+path)
                     for name in files
                     if pattern in name and name.endswith((".sh"))]
for f in files:
#    print f
    filename = f.split("/")[-1][:-3]
    # writing submit script file
    pathSubmitScript = path + "/submitFile_"+filename+".sub"
    codeSubmitScript = "universe = vanilla\n"
    codeSubmitScript += "should_transfer_files = IF_NEEDED\n"
    codeSubmitScript += "executable = /bin/bash\n"
    codeSubmitScript += "arguments = " + f + "\n"
    codeSubmitScript += "error = logs/" + filename + "_$(Cluster).out\n"
    codeSubmitScript += "output = logs/" + filename + "_$(Cluster).err\n"
    codeSubmitScript += "notification = Never\n"
    codeSubmitScript += "priority = 0\n"
    codeSubmitScript += "request_memory = 2000M\n"
    #codeSubmitScript += "request_disk = 2000M\n"
    codeSubmitScript += "queue"

    fileSubmitScript = open(pathSubmitScript, "w")
    fileSubmitScript.write(codeSubmitScript)
    fileSubmitScript.close()

    print "submitting script", f
    command = "condor_submit " + pathSubmitScript
    call(command.split())
