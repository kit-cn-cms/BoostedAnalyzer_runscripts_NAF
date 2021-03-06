outpath='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_2Btags/2018' # path of output of analyzer
scriptpath='legacy_2018_hdamp' # folder containing shell scripts that will have to be run on cluster
samplelist='ttH_legacy_samples_hdamp_2018.csv' # samples list
dataset_column='boosted_dataset' # run on the column with dataset or boosted_dataset?

cmsswcfgpathSL6='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_2Btags/CMSSW_10_2_18/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Legacy_2016_2017_2018_cfg.py'
cmsswpathSL6='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_2Btags/CMSSW_10_2_18/'

cmsswcfgpathSL7='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_2Btags/CC7/CMSSW_10_2_18/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Legacy_2016_2017_2018_cfg.py'
cmsswpathSL7='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_2Btags/CC7/CMSSW_10_2_18/'

dbs="prod/phys03" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=100000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='noSysts.txt'
nSystematicVariationsPerJob=3
ProduceMemNtuples=False
