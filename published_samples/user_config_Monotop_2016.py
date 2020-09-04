outpath='/nfs/dust/cms/user/mwassmer/MonoTop/ntuples_2016/' # path of output of analyzer
scriptpath='MonoTop_2016' # folder containing shell scripts that will have to be run on cluster
samplelist='../auto_samples_datasets_monotop_2016_v2.csv' # samples list
dataset_column='boosted_dataset' # run on the column with dataset or boosted_dataset?
cmsswcfgpath='/nfs/dust/cms/user/mwassmer/MonoTop/test/slc7/CMSSW_10_2_18/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Legacy_2016_2017_2018_cfg_sync.py'
cmsswpath='/nfs/dust/cms/user/mwassmer/MonoTop/test/slc7/CMSSW_10_2_18/'
dbs="prod/phys03" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=100000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='systematicVariations_no_sources.txt'
nSystematicVariationsPerJob=4
ProduceMemNtuples=False