# script to calculate rate factors for e.g. ME weights to ensure that there is only a shape change and not a normalization/yield change
import ROOT
import glob
import os
import csv
import optparse

parser = optparse.OptionParser()
parser.add_option("-i",dest="input",
    help = "input fraction file")
parser.add_option("-r",dest="ratefactorfile",
    help = "input ratefactor file")
parser.add_option("-y",dest="year",
    help = "year of data taking period")
(opts, args) = parser.parse_args()

directory = os.path.realpath(opts.input)
print("calculating ratefactors for ntuples in directory: {}".format(directory))

with open(opts.input, "r") as f:
    fraction_file = f.readlines()
sample_dict = {}
for line in fraction_file:
    entry = line.replace("\n","").replace("\"","").split(",")
    if not entry[0] in sample_dict:
        sample_dict[entry[0]] = {}
    sample_dict[entry[0]][entry[1]] = [entry[2], entry[3], entry[4], entry[5]]

with open(opts.ratefactorfile, "r") as f:
    rf_file = f.readlines()

if opts.year == "2017":
    translations_5fs = {
        "TTbb_Powheg_Openloops_DL": "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",
        "TTbb_Powheg_Openloops_new_pmx": "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8",
        "TTbb_4f_TTToHadronic_TuneCP5-Powheg-Openloops-Pythia8": "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_new_pmx",
        }
elif opts.year == "2018":
    translations_5fs = {
        "TTbb_4f_TTTo2l2nu_TuneCP5-Powheg-Openloops-Pythia8": "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
        "TTbb_4f_TTToSemiLeptonic_TuneCP5-Powheg-Openloops-Pythia8": "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
        "TTbb_4f_TTToHadronic_TuneCP5-Powheg-Openloops-Pythia8": "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
        }
elif opts.year == "2016":
    translations_5fs = {
        "TTbb_4f_TTTo2l2nu_TuneCP5-Powheg-Openloops-Pythia8": "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",
        "TTbb_4f_TTToSemiLeptonic_TuneCP5-Powheg-Openloops-Pythia8": "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8",
        "TTbb_4f_TTToHadronic_TuneCP5-Powheg-Openloops-Pythia8": "TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8",
        }
elif opts.year == "comb":
    translations_5fs = {
        "TTbbDL": "TTDL",
        "TTbbFH": "TTFH",
        "TTbbSL": "TTSL",
        }

else:
    sys.exit("need to specify a year for sample matching")

branches = [
    "nominal",
    "Weight_scale_variation_muR_1p0_muF_1p0",
    "Weight_scale_variation_muR_2p0_muF_1p0",
    "Weight_scale_variation_muR_2p0_muF_2p0",
    "Weight_scale_variation_muR_0p5_muF_1p0",
    "Weight_scale_variation_muR_0p5_muF_0p5",
    "Weight_scale_variation_muR_1p0_muF_2p0",
    "Weight_scale_variation_muR_1p0_muF_0p5",
    #"Weight_LHA_306000_nominal",
    #"Weight_LHA_306000_up",
    #"Weight_LHA_306000_down",
    #"Weight_LHA_320900_nominal",
    #"Weight_LHA_320900_up",
    #"Weight_LHA_320900_down"
]
#branches += ["Weight_pdf_variation_306{:03}".format(i) for i in range(0,103)]
#branches += ["Weight_pdf_variation_32{:04}".format(i) for i in range(900,1001)]
branches += [
    "GenWeight_fsr_Def_down",
    "GenWeight_fsr_Def_up",
    "GenWeight_fsr_Def_nom",
    "GenWeight_isr_Def_down",
    "GenWeight_isr_Def_up",
    "GenWeight_isr_Def_nom",
    ]


text = """
================================================
sample: {samplename}
variation: {varname}
fiducial XS change: {rf_fiducial}
inclusive XS change: {rf_inclusive}
----------------
fraction of tt+B: {ttbb_frac}
fraction of tt+B in 5FS sample: {ttbb_frac_5fs}
fraction of tt+B nominal: {nom_frac}
----------------
nom/varied tt+B fractions: {ratio_ttB_nom_vs_varied}
nom/varied tt+B fractions 5FS: {ratio_ttB_nom_vs_varied_5FS}
----------------
SL weight: {sl_weight}
================================================
"""
new_file = []
for line in rf_file:
    line = line.replace("\n","").replace("\"","")
    entries = line.split(",")
    if entries[0] == "sample":
        entries.append("fraction_ttB")
        entries.append("fraction_ttB_5FS")
        entries.append("fraction_ttC")
        entries.append("fraction_ttC_5FS")
        entries.append("fraction_ttC_nom")
        entries.append("fraction_ttC_5FS_nom")
        entries.append("fraction_ttLF")
        entries.append("fraction_ttLF_5FS")
        entries.append("fraction_ttLF_nom")
        entries.append("fraction_ttLF_5FS_nom")
        entries.append("ratio_ttB_nominal_vs_varied")
        entries.append("ratio_ttB_nominal_vs_varied_5FS")
        entries.append("ratio_ttB_5FS_vs_this")
        entries.append("ratio_ttB_5FS_vs_this_nom")
        entries.append("ratio_5FS_vs_this__nominal_vs_varied")
        entries.append("final_weight_sl_analysis")

    else:
        ttbb_frac = sample_dict[entries[0]][entries[1]][0]
        nom_frac = sample_dict[entries[0]]["nominal"][0]
        ttcc_frac = sample_dict[entries[0]][entries[1]][2]
        nom_cc_frac = sample_dict[entries[0]]["nominal"][2]
        ttlf_frac = sample_dict[entries[0]][entries[1]][3]
        nom_lf_frac = sample_dict[entries[0]]["nominal"][3]
        
        rf_fiducial = float(entries[2])
        rf_inclusive = float(entries[3])

        nonapplicable = False
        if entries[0].startswith("TTbb") and entries[1] in branches:
            samplename_5fs = translations_5fs[entries[0]]

            ttbb_frac_5fs = sample_dict[samplename_5fs][entries[1]][0]
            nom_frac_5fs = sample_dict[samplename_5fs]["nominal"][0]
            ttcc_frac_5fs = sample_dict[samplename_5fs][entries[1]][2]
            nom_cc_frac_5fs = sample_dict[samplename_5fs]["nominal"][2]
            ttlf_frac_5fs = sample_dict[samplename_5fs][entries[1]][3]
            nom_lf_frac_5fs = sample_dict[samplename_5fs]["nominal"][3]
        elif entries[0].startswith("TTTo"):
            ttbb_frac_5fs = sample_dict[entries[0]][entries[1]][0]
            nom_frac_5fs = sample_dict[entries[0]]["nominal"][0]
            ttcc_frac_5fs = sample_dict[entries[0]][entries[1]][2]
            nom_cc_frac_5fs = sample_dict[entries[0]]["nominal"][2]
            ttlf_frac_5fs = sample_dict[entries[0]][entries[1]][3]
            nom_lf_frac_5fs = sample_dict[entries[0]]["nominal"][3]
        else:
            ttbb_frac_5fs = -1.
            nom_frac_5fs = -1.
            ttcc_frac_5fs = -1.
            nom_cc_frac_5fs = -1.
            ttlf_frac_5fs = -1.
            nom_lf_frac_5fs = -1.
            nonapplicable = True

        ratio_ttB_nom_vs_varied = float(nom_frac)/float(ttbb_frac)
        ratio_ttB_nom_vs_varied_5FS = float(nom_frac_5fs)/float(ttbb_frac_5fs)
        ratio_ttB_5FS_vs_this = float(ttbb_frac_5fs)/float(ttbb_frac)
        ratio_ttB_5FS_vs_this_nom = float(nom_frac_5fs)/float(nom_frac)
        ratio_5FS_this_nominal_vs_varied = ratio_ttB_5FS_vs_this_nom/ratio_ttB_5FS_vs_this

        if nonapplicable:
            ratio_ttB_nom_vs_varied_5FS = -1.
            ratio_ttB_5FS_vs_this = -1.
            ratio_ttB_5FS_vs_this_nom = -1.
            ratio_5FS_this_nominal_vs_varied = -1.
        
        entries.append(str(ttbb_frac))
        entries.append(str(ttbb_frac_5fs))
        entries.append(str(ttcc_frac))
        entries.append(str(ttcc_frac_5fs))
        entries.append(str(nom_cc_frac))
        entries.append(str(nom_cc_frac_5fs))
        entries.append(str(ttlf_frac))
        entries.append(str(ttlf_frac_5fs))
        entries.append(str(nom_lf_frac))
        entries.append(str(nom_lf_frac_5fs))
        entries.append(str(ratio_ttB_nom_vs_varied))
        entries.append(str(ratio_ttB_nom_vs_varied_5FS))
        entries.append(str(ratio_ttB_5FS_vs_this))
        entries.append(str(ratio_ttB_5FS_vs_this_nom))
        entries.append(str(ratio_5FS_this_nominal_vs_varied))
        
        sl_weight = 1.
        if entries[0].startswith("TTbb"):
            if entries[1] in branches:
                sl_weight = rf_fiducial / ratio_ttB_nom_vs_varied_5FS
            else:
                sl_weight = rf_fiducial
        else:
            sl_weight = rf_inclusive

        entries.append(str(sl_weight))
        print(text.format(
            **{"samplename": entries[0], "varname": entries[1],
                "ttbb_frac": ttbb_frac,
                "nom_frac": nom_frac,
                "ttbb_frac_5fs": ttbb_frac_5fs,
                "ratio_ttB_nom_vs_varied": ratio_ttB_nom_vs_varied,
                "ratio_ttB_nom_vs_varied_5FS": ratio_ttB_nom_vs_varied_5FS,
                "rf_fiducial": rf_fiducial,
                "rf_inclusive": rf_inclusive,
                "sl_weight": sl_weight}))


    new_file.append(",".join(entries))

outf = opts.ratefactorfile.replace(".csv","_with_correction.csv")
with open(outf, "w") as f:
    f.write("\n".join(new_file))
print("wrote new file to {}".format(outf))
