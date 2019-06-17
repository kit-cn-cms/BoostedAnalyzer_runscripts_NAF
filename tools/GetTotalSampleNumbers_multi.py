import ROOT
import sys
import urllib2
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def GetTotalSampleNumbers(name):
    files=[]
    for file in name:
        files.append(file)
    usexroot=True
    totalNumber=0
    totweights = 0
    totevents = 0
    FileList=[]
    print files
    if usexroot:
      #print "in xroot condition"
      for f in files:
            FileList.append("root://xrootd-cms.infn.it//"+f)
      #print "Filelist ",FileList
    
    else:
      #print "in else condition"
      FileList=files

    print "N files ", len(FileList)
    nfiles=len(FileList)
    print "counting events"
    ifile=0
    ##now count the events
    if(nfiles>0):
	for f in FileList:
	    print f
	    if usexroot:
	      tf=ROOT.TFile.Open(str(f))
	    else:
	      tf=ROOT.TFile(str(f),"READ")
	    tree=tf.Get("Events")
	    if tree==None:
	      continue
	    tree.Draw("1.>>totweights(1,0,2)","GenEventInfoProduct_generator__SIM.obj.weight()","goff")
	    weights = ROOT.gDirectory.Get("totweights")
	    totweights += weights.Integral()
	    totevents += weights.GetEntries()
	    print "done with File ", ifile, "/", nfiles, f
	    cumulFraction=totweights/totevents
	    print "sum of entries, sum of gen weights, cumulFraction(sow/soe) ",totevents,totweights, cumulFraction
	    tf.Close()
	    ifile+=1
    else:
	cumulFraction=0.

    
    #print "total number of positive events: "+str(int(totalPos))
    #print "total number of negative events: "+str(int(totalNeg))
    #print "total number of events: "+str(int(totalNumber))
    print "returning fraction: "+str(cumulFraction)
    return cumulFraction
