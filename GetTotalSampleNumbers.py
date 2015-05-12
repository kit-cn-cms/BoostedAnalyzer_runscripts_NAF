import ROOT
import sys

if len(sys.argv)<2:
  print "Usage:"
  print "python GetTotalSampleNumbers LIST_OF_MiniAOD_FILES"
  exit(0)

files=sys.argv[1:]
print files

totalNumber=0
#hnE=ROOT.TH1F("hnE","hnE",100,-10,10)

for f in files:
  tf=ROOT.TFile(str(f),"READ")
  tree=tf.Get("Events")
  hpE=ROOT.TH1D("hpE","hpE",100,-10,10)
  hnE=ROOT.TH1D("hnE","hnE",100,-10,10)
  tree.Project("hpE","GenEventInfoProduct_generator__SIM.obj.weights_","GenEventInfoProduct_generator__SIM.obj.weights_>0")
  tree.Project("hnE","GenEventInfoProduct_generator__SIM.obj.weights_","GenEventInfoProduct_generator__SIM.obj.weights_<0")
  np=hpE.GetEntries()
  nn=hnE.GetEntries()
  print np, nn
  totalNumber+=np
  totalNumber-=nn
  tf.Close()

print "total number of events: "+str(int(totalNumber))

