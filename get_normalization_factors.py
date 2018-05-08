# script to calculate rate factors for e.g. ME weights to ensure that there is only a shape change and not a normalization/yield change

import ROOT
import glob
import os
import csv

directory="/nfs/dust/cms/user/mwassmer/ntuples/weights/"
samples=glob.glob(directory+"*")
#print samples
files=[]
for sample in samples:
    files.append(glob.glob(sample+"/*.root"))
    
############################################################    
sample_dict={}
with open('auto_samples_complete.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        sample_dict[row[0]]=row[1]
    
############################################################
    
#print files
fobj_out=open("rate_factors_final/rate_factors.csv","w")
fobj_out.write('name,weight,factor'+'\n')

for i in range(len(samples)):
    sample=samples[i].replace(directory,"")
    if len(files[i])<2:
    	continue
    print sample
    if not os.path.isdir("rate_factors_final/"+sample):
        os.mkdir("rate_factors_final/"+sample)
    file_=ROOT.TChain("MVATree","MVATree")
    for k in range(len(files[i])):
        file_.Add(files[i][k])
    print file_.GetEntries()
    if file_.GetEntries()<50000:
    	print "not enough events in tree"
    	continue
    #file_.Draw("Weight_CSV")
    
    for branch in file_.GetListOfBranches():
        branch_name=branch.GetName()
        print branch_name
        if branch_name.find("Weight")==-1:
            continue
        elif branch_name.find("CSV")!=-1:
            continue
        elif branch_name.find("Electron")!=-1:
            continue
        elif branch_name.find("Muon")!=-1:
            continue
        elif branch_name.find("Top")!=-1:
            continue
        elif branch_name.find("PU")!=-1:
            continue
        elif branch_name.find("pu")!=-1:
            continue
        elif branch_name.find("hdamp")!=-1:
            continue
        elif branch_name.find("Lepton")!=-1:
            continue
        elif branch_name.find("XS")!=-1:
            continue
        elif branch_name=="Weight":
            continue
        canvas=ROOT.TCanvas()
        file_.DrawClone(branch_name+">>"+sample+branch_name+"(30,0,3)")
        test = ROOT.gROOT.FindObject(sample+branch_name)
        try:
            if test.GetMean()>0.:
                factor = 1./test.GetMean()
            else: 
                factor = 1.
        except AttributeError:
            continue
        fobj_out.write('"'+str(sample_dict[sample])+'"'+","+str(branch_name)+","+str(factor)+'\n')
        #print 1./test.GetMean()
        canvas.Print("rate_factors_final/"+sample+"/"+branch_name+".pdf")
        del canvas
    del file_
    
fobj_out.close






















"""
    for branch in file_.GetListOfBranches():
        branch_name=branch.GetName()
	print branch_name
        if branch_name.find("Weight")==-1:
            continue
        #canvas=ROOT.TCanvas()
        file_.Draw(branch_name+">>"+sample+branch_name+"(30,0,3)","","")
        test = ROOT.gROOT.FindObject(sample+branch_name)
        #print branch_name,test.GetMean()
        canvas.Print("rate_factors/"+sample+"/"+branch_name+".pdf")
"""
