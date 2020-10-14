outpath='/nfs/dust/cms/user/vdlinden/legacyTTZ/ntupleProduction/ttZ_2016' # path of output of analyzer
scriptpath='ntuples_2016' # folder containing shell scripts that will have to be run on cluster
samplelist='ttZ_legacy_samples_2016.csv' # samples list
dataset_column='boosted_dataset' # run on the column with dataset or boosted_dataset?

cmsswcfgpath='/nfs/dust/cms/user/vdlinden/legacyTTZ/ntupleProduction/CMSSW/CMSSW_10_2_18/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-ttZ_2017.py'
cmsswpath='/nfs/dust/cms/user/vdlinden/legacyTTZ/ntupleProduction/CMSSW/CMSSW_10_2_18/'

dbs="prod/phys03" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=100000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='noSysts.txt'
nSystematicVariationsPerJob=3
ProduceMemNtuples=False
