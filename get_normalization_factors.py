# script to calculate rate factors for e.g. ME weights to ensure that there is only a shape change and not a normalization/yield change

import ROOT
import glob
import os
import csv

directory = "/nfs/dust/cms/user/kelmorab/ttH_2018/ntuples_v5/"
samples = glob.glob(directory + "TT*")
print (samples)
files = []
for i in range(len(samples)):
    files.append(glob.glob(samples[i] + "/*nominal*.root"))

############################################################
sample_dict = {}
with open("ttH_2018_samples_221018.csv", "rb") as f:
    reader = csv.reader(f)
    for row in reader:
        sample_dict[row[0]] = row[1]

############################################################

# print(files)
fobj_out = open("rate_factors_final/rate_factors.csv", "w")
fobj_out.write("name,weight,factor" + "\n")

file_ = ROOT.TChain("MVATree", "MVATree")

branches = [
    "Weight_scale_variation_muR_1p0_muF_1p0",
    "Weight_scale_variation_muR_2p0_muF_1p0",
    "Weight_scale_variation_muR_0p5_muF_1p0",
    "Weight_scale_variation_muR_1p0_muF_2p0",
    "Weight_scale_variation_muR_1p0_muF_0p5",
    "Weight_LHA_306000_nominal",
    "Weight_LHA_306000_up",
    "Weight_LHA_306000_down",
]

for i in range(len(samples)):
    sample = samples[i].replace(directory, "")
    if len(files[i]) < 2:
        continue
    print (sample)
    if not os.path.isdir("rate_factors_final/" + sample):
        os.mkdir("rate_factors_final/" + sample)
    for k in range(len(files[i])):
        file_.Add(files[i][k])
    print (file_.GetEntries())
    if file_.GetEntries() < 50000:
        print ("not enough events in tree")
        file_.Reset()
        continue
    # file_.Draw("Weight_CSV")
    # file_.GetListOfBranches().Print()
    for branch in branches:
        branch_name = branch
        print (branch_name)
        if branch_name.find("muR") != -1 or branch_name.find("muF") != -1 or branch_name.find("LHA_306000") != -1:
            # canvas=ROOT.TCanvas()
            print ("!!!!!!!!!", branch_name, "!!!!!!!!!!")
            file_.Draw(
                "1." + ">>" + sample + branch_name + "(1,0,2)",
                "Weight_XS*Weight_GEN_nom*" + branch_name + "*(" + branch_name + ">0.)" + "*(" + branch_name + "<2.)",
                "goff",
            )
            file_.Draw(
                "1." + ">>" + sample + branch_name + "nom" + "(1,0,2)",
                "Weight_XS*Weight_GEN_nom" + "*(" + branch_name + ">0.)" + "*(" + branch_name + "<2.)",
                "goff",
            )
            test_var = ROOT.gDirectory.Get(sample + branch_name)
            test_nom = ROOT.gDirectory.Get(sample + branch_name + "nom")
            try:
                if test_nom.Integral() > 0.0 and test_var.Integral():
                    factor = test_nom.Integral() / test_var.Integral()
                    # print(factor)
                else:
                    factor = 1.0
            except AttributeError:
                factor = 1.0
            fobj_out.write('"' + str(sample_dict[sample]) + '"' + "," + str(branch_name) + "," + str(factor) + "\n")
        # print(1./test.GetMean())
        # canvas.Print("rate_factors_final/"+sample+"/"+branch_name+".pdf")
        # del canvas
    file_.Reset()

fobj_out.close
