import sys
inf=sys.argv[1]

infile=open(inf)
inlist=list(infile)

totalReal=0
totalCPU=0
lastCPUTime=0
lastRealTime=0

for line in inlist:
  if "CP time" in line:
    sl=line.replace("\n","").replace(",","").split(" ")
    print sl
    lastCPUTime=float(sl[-1])
    
  if not "time spent in" in line:
    continue
  splitline=line.replace("\n","").replace(",","").split(" ")
  #print splitline
  #print splitline[-1], splitline[-4]
  totalCPU+=float(splitline[-1])
  totalReal+=float(splitline[-4])
  print totalCPU, totalReal
  
  
print ""
print "cpu", totalCPU
print "real", totalReal
print "loop cpu time", lastCPUTime
print "processor fraction ", totalCPU/lastCPUTime