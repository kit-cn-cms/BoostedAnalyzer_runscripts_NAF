outpath='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_v2/2017' # path of output of analyzer
scriptpath='legacy_2017_v2' # folder containing shell scripts that will have to be run on cluster
samplelist='ttH_legacy_samples_2017_incomplete.csv' # samples list
dataset_column='boosted_dataset' # run on the column with dataset or boosted_dataset?
cmsswcfgpath='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_v2/CMSSW_9_4_13/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Legacy_2016_2017_2018_cfg.py'
cmsswpath='/nfs/dust/cms/user/swieland/ttH_legacy/ntuple_v2/CMSSW_9_4_13/'
dbs="prod/phys03" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=100000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='systematicVariations.txt'
nSystematicVariationsPerJob=4
ProduceMemNtuples=False
