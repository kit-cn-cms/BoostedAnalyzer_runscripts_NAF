import numpy as np
import optparse
import pandas
import os

template = """
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = '{requestName}'

config.General.workArea = 'crab_ntuple'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/nfs/dust/cms/user/vdlinden/ttZAnalysis/CMSSW_ntupling/CMSSW_10_2_13/src/BoostedTTH/BoostedAnalyzer/test/ntupling_ttZAnalysis.py'
config.JobType.outputFiles = {outFiles}
# config.JobType.maxJobRuntimeMin = 2800
config.JobType.maxMemoryMB = 2000
config.JobType.pyCfgParams = ["outName=ntuples", "weight={weight}", "isData={isData}", "maxEvents=999999999", "globalTag={globalTag}", "systematicVariations={variations}", "ProduceMemNtuples=False", "dataEra={era}"]
config.JobType.sendPythonFolder=True

config.Data.inputDataset = "{dataset}"
config.Data.inputDBS = '{dbs}'
config.Data.unitsPerJob = {nfilesperjob}
config.Data.splitting = 'FileBased'
config.Data.publication = False
config.Data.publishDBS = 'phys03'
config.Data.outputDatasetTag = 'KIT_ttzbb_sl_private_ntuples_2018'

config.User.voGroup = 'dcms'

config.Site.storageSite = 'T2_DE_DESY'
"""

parser = optparse.OptionParser()
parser.add_option("-s", "--systematics", dest="systematics",
    help = "txt file with systematics")
parser.add_option("-n", "--nsystsperjob", dest="nsysts", default = 4,
    help = "number of systematic variations per job")
parser.add_option("-f", "--nfilesperjob", dest="nfiles", default = 2,
    help = "number of files per job")
parser.add_option("-d", "--dataset", dest="dataset",
    help = "samples csv of datasets")
parser.add_option("-o", "--output", dest="outDir",
    help = "output directory")
parser.add_option("--useskims", dest="use_skimmed_files", default = False, action = "store_true",
    help = "use skimmed files instead of global dataset")
(opts, args) = parser.parse_args()

# loading csv file
csv = pandas.read_csv(opts.dataset, skip_blank_lines = True, header = 0)

# managing systematics
with open(opts.systematics, "r") as f:
    systematics = f.readlines()
    systematics = [s.replace(" ","").replace("\n","") for s in systematics if not s == ""]
# add nominal
if not "nominal" in systematics:
    systematics = ["nominal"]+systematics
# split into groups of opts.nsysts
while len(systematics)%int(opts.nsysts)!=0: systematics.append("")
systematics = np.array(systematics)
systematics = systematics.reshape(-1,int(opts.nsysts))

# generate output directory
if not os.path.exists(opts.outDir):
    os.makedirs(opts.outDir)

# naming for output files
naming = "ntuples_{syst}_Tree.root"

# loop over datasets
for dataset in csv.iterrows():
    if not type(dataset[1]["name"]) == str: continue
    
    print("="*50)
    print("generating config for {}".format(dataset[1]["name"]))

    # name for request
    requestBaseName = dataset[1]["name"]+"_ntuples_private"

    # get dataset and database
    if opts.use_skimmed_files:
        datapaths = dataset[1]["boosted_dataset"].split(",")
        database  = "phys03"
    else:
        datapaths = dataset[1]["dataset"].split(",")
        database  = "global"
    print("database used: {}\n".format(database))

    # loop over datasets
    for dataID, data in enumerate(datapaths):

        # loop over syst groups
        for systID, systs in enumerate(systematics):

            # collect syst names
            outFiles = []
            for s in systs:
                if s == "": continue
                elif s == "nominal": 
                    outFiles.append(naming.format(syst=s))
                else:
                    outFiles.append(naming.format(syst=s+"up"))
                    outFiles.append(naming.format(syst=s+"down"))
            variations = ",".join([s for s in systs if not s == ""])

            # collect config info
            config = {}
            config["requestName"]   = requestBaseName+"_"+str(dataID)+"_"+str(systID)
            config["dataset"]       = data
            config["outFiles"]      = outFiles
            config["variations"]    = variations
            config["weight"]        = dataset[1]["weight"]
            config["nfilesperjob"]  = int(opts.nfiles)
            config["dbs"]           = database
            config["isData"]        = dataset[1]["isData"]
            config["globalTag"]     = dataset[1]["globalTag"]
            config["era"]           = int(dataset[1]["run"])

            # write template
            crabjob = template.format(**config)

            # write to output file
            outfile = opts.outDir+"/"+config["requestName"]+"_crab.py"
            with open(outfile, "w") as f:
                f.write(crabjob)
            print("\twrote crab config {}".format(outfile))



















