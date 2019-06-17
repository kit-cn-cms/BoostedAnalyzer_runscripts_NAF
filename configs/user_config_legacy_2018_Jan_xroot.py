outpath='/nfs/dust/cms/user/vdlinden/legacyTTH/ntuples/legacy_2018_ttZ/' # path of output of analyzer
scriptpath='legacy_2018_ttZ_xroot' # folder containing shell scripts that will have to be run on cluster
samplelist='../ttH_legacy_samples_2018_ttZ_Jan_xroot.csv' # samples list
dataset_column='dataset' # run on the column with dataset or boosted_dataset?
cmsswcfgpath='/nfs/dust/cms/user/vdlinden/legacyTTH/CMSSW/CMSSW_10_2_13/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Legacy_2016_2017_2018_cfg.py'
cmsswpath='/nfs/dust/cms/user/vdlinden/legacyTTH/CMSSW/CMSSW_10_2_13/'
dbs="prod/global" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=100000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='totalJECSysts.txt'
nSystematicVariationsPerJob=3
ProduceMemNtuples=False
