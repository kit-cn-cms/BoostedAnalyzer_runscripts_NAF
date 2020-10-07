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

# print(files)
if not os.path.exists(opts.output):
    os.makedirs(opts.output)

rffile = opts.output+"/ratefactor_ratios.csv"
fobj_out = open(rffile, "w")
fobj_out.write("sample,variation,ttB_frac,ttOther_frac,ttC_frac,ttLF_frac" + "\n")

file_ = ROOT.TChain("MVATree", "MVATree")

branches = [
    "nominal",
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
    if not sample in sample_dict:
        print("sample {} not in sample list".format(sample))
        continue
    print("\n"*4+"="*50)
    print (sample)
    print("\n")

    # define fiducial selection:
    selection_ttbb = "1.*(GenEvt_I_TTPlusBB>=1)"
    selection_ttother = "1.*(GenEvt_I_TTPlusBB==0)"
    selection_ttlf = "1.*(GenEvt_I_TTPlusBB==0)*(GenEvt_I_TTPlusCC==0)"
    selection_ttcc = "1.*(GenEvt_I_TTPlusBB==0)*(GenEvt_I_TTPlusCC==1)"
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
        branch_weight = "1." if branch_name == "nominal" else branch_name       
        print ("\tchecking branch {}".format(branch_name))

        if not branch_name in file_branches and not branch_name == "nominal":
            print("branch {} not in file - skipping.".format(branch_name))
            continue
        #canvas=ROOT.TCanvas()
        frac_ttbb = -1.
        frac_ttother = -1.
        frac_ttcc = -1.
        frac_ttlf = -1.

        if sample.startswith("TT") or sample.startswith("TTbb"):
            test_ttbb = ROOT.TH1D(sample+branch_name+"ttbb",sample+branch_name+"ttbb",1,-20,20)
            test_ttother = ROOT.TH1D(sample+branch_name+"ttother",sample+branch_name+"ttother",1,-20,20)
            test_ttcc = ROOT.TH1D(sample+branch_name+"ttcc",sample+branch_name+"ttcc",1,-20,20)
            test_ttlf = ROOT.TH1D(sample+branch_name+"ttlf",sample+branch_name+"ttlf",1,-20,20)
            file_.Draw(
                "1."+">>"+sample+branch_name+"ttbb",
                selection_ttbb+"*Weight_GEN_nom*"+branch_weight ,
                "goff",
            )
            file_.Draw(
                "1."+">>"+sample+branch_name+"ttother",
                selection_ttother+"*Weight_GEN_nom*"+branch_weight,
                "goff",
            )
            file_.Draw(
                "1."+">>"+sample+branch_name+"ttcc",
                selection_ttcc+"*Weight_GEN_nom*"+branch_weight,
                "goff",
            )
            file_.Draw(
                "1."+">>"+sample+branch_name+"ttlf",
                selection_ttlf+"*Weight_GEN_nom*"+branch_weight,
                "goff",
            )
            try:
                if test_ttbb.Integral() > 0.0 and test_ttother.Integral() > 0.0:
                    frac_ttbb = test_ttbb.Integral() / (test_ttbb.Integral()+test_ttother.Integral())
                    frac_ttother = test_ttother.Integral() / (test_ttbb.Integral()+test_ttother.Integral())
                    frac_ttcc = test_ttcc.Integral() / (test_ttbb.Integral()+test_ttother.Integral())
                    frac_ttlf = test_ttlf.Integral() / (test_ttbb.Integral()+test_ttother.Integral())
                    # print(factor)
            except:
                pass

        line = "{},{},{:.6f},{:.6f},{:.6f},{:.6f}\n".format(
            sample_dict[sample], branch_name, frac_ttbb, frac_ttother, frac_ttcc, frac_ttlf)
        print("\t\t"+line)
        fobj_out.write(line)
        # print(1./test.GetMean())
        #canvas.Print(opts.output+"/"+sample+"/"+branch_name+".pdf")
        #del canvas
    file_.Reset()

fobj_out.close

