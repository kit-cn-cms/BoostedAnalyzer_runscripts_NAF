outpath='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_JECgroups/2016' # path of output of analyzer
scriptpath='legacy_2016' # folder containing shell scripts that will have to be run on cluster
samplelist='ttH_legacy_samples_2016.csv' # samples list
dataset_column='boosted_dataset' # run on the column with dataset or boosted_dataset?

cmsswcfgpathSL6='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_JECgroups/CMSSW_10_2_18/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Legacy_2016_2017_2018_cfg.py'
cmsswpathSL6='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_JECgroups/CMSSW_10_2_18/'

cmsswcfgpathSL7='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_JECgroups/CC7/CMSSW_10_2_18/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Legacy_2016_2017_2018_cfg.py'
cmsswpathSL7='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_JECgroups/CC7/CMSSW_10_2_18/'

dbs="prod/phys03" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=100000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='systematicVariations_new.txt'
nSystematicVariationsPerJob=4
ProduceMemNtuples=False
