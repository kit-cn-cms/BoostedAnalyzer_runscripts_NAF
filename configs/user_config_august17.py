outpath='/nfs/dust/cms/user/mwassmer/ntuples/august17/' # path of output of analyzer
scriptpath='august17' # folder containing shell scripts that will have to be run on cluster
samplelist='../auto_samples_complete.csv' # samples list
dataset_column='dataset' # run on the column with dataset or boosted_dataset?
cmsswcfgpath='/nfs/dust/cms/user/mwassmer/crab_ntuples/CMSSW_8_0_26_patch2/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Spring17_cfg.py'
cmsswpath='/nfs/dust/cms/user/mwassmer/crab_ntuples/CMSSW_8_0_26_patch2/'
dbs="prod/global" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=50000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='systematicVariations.txt'
nSystematicVariationsPerJob=4
