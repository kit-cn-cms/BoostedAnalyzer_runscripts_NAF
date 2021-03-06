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
        if len(row) == 0: continue
        sample_dict[row[0]] = row[0]

############################################################

line_template = "{sample},{branch},{fiducial},{inclusive}\n"

# print(files)
if not os.path.exists(opts.output):
    os.makedirs(opts.output)

rffile = opts.output+"/ratefactors_new.csv"
fobj_out = open(rffile, "w")
fobj_out.write("sample,variation,fiducial_xs_norm,inclusive_xs_norm" + "\n")

file_ = ROOT.TChain("MVATree", "MVATree")

branches = [
    "Weight_scale_variation_muR_1p0_muF_1p0",
    "Weight_scale_variation_muR_2p0_muF_1p0",
    "Weight_scale_variation_muR_2p0_muF_2p0",
    "Weight_scale_variation_muR_0p5_muF_1p0",
    "Weight_scale_variation_muR_0p5_muF_0p5",
    "Weight_scale_variation_muR_1p0_muF_2p0",
    "Weight_scale_variation_muR_1p0_muF_0p5",
    "Weight_LHA_306000_nominal",
    "Weight_LHA_306000_up",
    "Weight_LHA_306000_down",
    "Weight_LHA_320900_nominal",
    "Weight_LHA_320900_up",
    "Weight_LHA_320900_down"
]
branches += ["Weight_pdf_variation_306{:03}".format(i) for i in range(0,103)]
branches += ["Weight_pdf_variation_32{:04}".format(i) for i in range(900,1001)]
branches += [
    "GenWeight_fsr_Def_down",
    "GenWeight_fsr_Def_up",
    "GenWeight_fsr_Def_nom",
    "GenWeight_isr_Def_down",
    "GenWeight_isr_Def_up",
    "GenWeight_isr_Def_nom",
    ]

for i in range(len(samples)):
    sample = samples[i].replace(directory, "").replace("/","")
    print("\n"*4+"="*50)
    print (sample)
    print("\n")
    if not sample in sample_dict: continue
    # define fiducial selection:
    selection = "1."
    if sample.startswith("TTTo"):
        selection = "1.*(GenEvt_I_TTPlusBB==0)"
    if sample.startswith("TTbb"):
        selection = "1.*(GenEvt_I_TTPlusBB>=1)"
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


        ### FIDUCIAL
        #canvas=ROOT.TCanvas()
        test_var = ROOT.TH1D(sample+branch_name, sample+branch_name, 1, -20, 20)
        test_nom = ROOT.TH1D(sample+branch_name+"nom", sample+branch_name+"nom", 1, -20, 20)
        file_.Draw(
            "1."+">>"+sample+branch_name,
            selection+"*Weight_GEN_nom*"+branch_name,
            "goff",
        )
        file_.Draw(
            "1."+">>"+sample+branch_name+"nom",
            selection+"*Weight_GEN_nom",
            "goff",
        )
        try:
            if test_nom.Integral() > 0.0 and test_var.Integral() > 0.0:
                fiducial_factor = test_nom.Integral() / test_var.Integral()
            else:
                fiducial_factor = 1.0
        except AttributeError:
            fiducial_factor = 1.0

        ### INCLUSIVE
        #canvas=ROOT.TCanvas()
        test_var = ROOT.TH1D(sample+branch_name+"incl", sample+branch_name, 1, -20, 20)
        test_nom = ROOT.TH1D(sample+branch_name+"incl"+"nom", sample+branch_name+"nom", 1, -20, 20)
        file_.Draw(
            "1."+">>"+sample+branch_name+"incl",
            "Weight_GEN_nom*"+branch_name,
            "goff",
        )
        file_.Draw(
            "1."+">>"+sample+branch_name+"incl"+"nom",
            "Weight_GEN_nom",
            "goff",
        )
        try:
            if test_nom.Integral() > 0.0 and test_var.Integral() > 0.0:
                inclusive_factor = test_nom.Integral() / test_var.Integral()
                # print(factor)
            else:
                inclusive_factor = 1.0
        except AttributeError:
            inclusive_factor = 1.0

        line = line_template.format(**{
            "sample": sample_dict[sample],
            "branch": branch_name,
            "fiducial": str(fiducial_factor),
            "inclusive": str(inclusive_factor)})
        print("\t\t"+line)
        fobj_out.write(line)
    file_.Reset()

fobj_out.close

