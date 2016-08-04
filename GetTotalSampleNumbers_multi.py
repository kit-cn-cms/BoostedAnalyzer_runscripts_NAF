import ROOT
import sys
import urllib2

"""
if len(sys.argv)<2:
  print "Usage:"
  print "python GetTotalSampleNumbers [-x] LIST_OF_MiniAOD_FILES|DATASET_NAMES_LIKE_IN_DAS"
  print "-x uses xroot to open the files returned by the DAS Query "
  print "e.g. /ttHJetTobb_M120_13TeV_amcatnloFXFX_madspin_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"
  exit(0)
"""
def GetTotalSampleNumbers(name):
    files=[]
    files.append(name)
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
        query=f.replace("dataset=/","")
        if query[0]=="/":
          query=query.lstrip("/")
        queryOutput=urllib2.urlopen("https://cmsweb.cern.ch/das/makepy?dataset=/"+query+"&instance=prod/global")
        qlines=list(queryOutput)
        #print "qlines ",qlines
        for qline in qlines:
          if "root" in qline and "store" in qline:
            FileList.append("root://xrootd-cms.infn.it//"+qline.replace("'","").replace(",","").replace("]","").replace(";","").replace(" ","").replace(")","").strip())
      #print "Filelist ",FileList
      for raw in FileList:
        print raw
    else:
      #print "in else condition"
      FileList=files

    print "N files ", len(FileList)
    nfiles=len(FileList)
    print "counting events"
    ifile=0
    ##write files where the tree could not be found in this file
    blacklist=open("blacklist.txt","w")
    ##now count the events
    for f in FileList[0:10]:
      print f
      if usexroot:
        tf=ROOT.TFile.Open(str(f))
      else:
        tf=ROOT.TFile(str(f),"READ")
      tree=tf.Get("Events")
      if tree==None:
        blacklist.write(f+"\n")
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

    blacklist.close()

    totalNumber=totalPos-totalNeg
    print "total number of positive events: "+str(int(totalPos))
    print "total number of negative events: "+str(int(totalNeg))
    print "total number of events: "+str(int(totalNumber))
    print "check the blacklist.txt file for problematic input samples."
    print "get-filenames.sh will ignore files in this list."

    return cumulFraction
