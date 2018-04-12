import ROOT
import sys
import urllib2
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def GetTotalSampleNumbers(name):
    files=[]
    for file in name:
        files.append(file)
    #files.append(name)
    usexroot=True
    totalNumber=0
    totalPos=0
    totalNeg=0
    #hnE=ROOT.TH1F("hnE","hnE",100,-10,10)
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
	for f in FileList[0:10]:
	    print f
	    if usexroot:
	      tf=ROOT.TFile.Open(str(f))
	    else:
	      tf=ROOT.TFile(str(f),"READ")
	    tree=tf.Get("Events")
	    if tree==None:
	      continue
	    hpE=ROOT.TH1D("hpE","hpE",100,-10,10)
	    hnE=ROOT.TH1D("hnE","hnE",100,-10,10)
	    tree.Project("hpE","GenEventInfoProduct_generator__SIM.obj.weights_","GenEventInfoProduct_generator__SIM.obj.weights_>0")
	    tree.Project("hnE","GenEventInfoProduct_generator__SIM.obj.weights_","GenEventInfoProduct_generator__SIM.obj.weights_<0")
	    np=hpE.GetEntries()
	    nn=hnE.GetEntries()
	    print "done with File ", ifile, "/", nfiles, f
	    totalPos+=np
	    totalNeg+=nn
	    cumulFraction=(totalPos-totalNeg)/(totalPos+totalNeg)
	    print "npos, nneg, cumulFraction ", np, nn, cumulFraction
	    tf.Close()
	    ifile+=1
	totalNumber=totalPos-totalNeg   
    else:
	totalPos=0
	totalNeg=0
	cumulFraction=0

    
    print "total number of positive events: "+str(int(totalPos))
    print "total number of negative events: "+str(int(totalNeg))
    print "total number of events: "+str(int(totalNumber))

    return cumulFraction
