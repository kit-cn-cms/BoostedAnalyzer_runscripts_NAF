# script to calculate rate factors for e.g. ME weights to ensure that there is only a shape change and not a normalization/yield change
import ROOT
import glob
import os
import csv
import optparse

parser = optparse.OptionParser()
parser.add_option("-i",dest="input",
    help = "directory with inclusive ntuples. In this directory should be one subdirectory per sample")
parser.add_option("-s",dest="samplefile",
    help = "samplefile from runscripts repository")
parser.add_option("-o",dest="output",
    help = "output directory")
(opts, args) = parser.parse_args()

directory = os.path.realpath(opts.input)
print("calculating ratefactors for ntuples in directory: {}".format(directory))

# globbing samplies
samples = glob.glob(directory + "/*")
print("samples:")
for s in samples: print("\t"+s)

files = []
for i in range(len(samples)):
    files.append(glob.glob(samples[i] + "/*nominal*.root"))

############################################################
sample_dict = {}
with open(opts.samplefile, "rb") as f:
    reader = csv.reader(f)
    for row in reader:
        sample_dict[row[0]] = row[1]

############################################################

# print(files)
if not os.path.exists(opts.output):
    os.makedirs(opts.output)

rffile = opts.output+"/ratefactors.csv"
fobj_out = open(rffile, "w")
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
    "Weight_LHA_320900_nominal",
    "Weight_LHA_320900_up",
    "Weight_LHA_320900_down"
]

for i in range(len(samples)):
    sample = samples[i].replace(directory, "").replace("/","")
    print("\n"*4+"="*50)
    print (sample)
    print("\n")
    #if not os.path.exists(opts.output+"/"+sample):
    #    os.makedirs(opts.output+"/"+sample)

    for k in range(len(files[i])):
        file_.Add(files[i][k])

    print("number of entries: {}".format(file_.GetEntries()))
    if file_.GetEntries() < 50000:
        print ("not really enough events in tree")
        #file_.Reset()
        #continue

    file_branches = [b.GetName() for b in list(file_.GetListOfBranches())]
    # file_.Draw("Weight_CSV")
    # file_.GetListOfBranches().Print()
    for branch in branches:
        branch_name = branch
        print ("\tchecking branch {}".format(branch_name))

        if not branch_name in file_branches:
            print("branch {} not in file - skipping.".format(branch_name))
            continue
        #canvas=ROOT.TCanvas()
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

        line = '"' + str(sample_dict[sample]) + '"' + "," + str(branch_name) + "," + str(factor) + "\n"
        print("\t\t"+line)
        fobj_out.write(line)
        # print(1./test.GetMean())
        #canvas.Print(opts.output+"/"+sample+"/"+branch_name+".pdf")
        #del canvas
    file_.Reset()

fobj_out.close

