outpath='/nfs/dust/cms/user/vdlinden/legacyTTH/ntuples/sfDerivation_full/2016' # path of output of analyzer
scriptpath='ratefactors_full/2016' # folder containing shell scripts that will have to be run on cluster
samplelist='ttH_legacy_ratefactors_2016.csv' # samples list
dataset_column='dataset' # run on the column with dataset or boosted_dataset?
cmsswcfgpath='/nfs/dust/cms/user/vdlinden/legacyTTH/ratefactors_legacy/CMSSW_10_2_18/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ratefactors.py'
cmsswpath='/nfs/dust/cms/user/vdlinden/legacyTTH/ratefactors_legacy/CMSSW_10_2_18/'
dbs="prod/global" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=123456 # min number of events per job 
#max_events_total=10000000
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='noSysts.txt'
nSystematicVariationsPerJob=4
ProduceMemNtuples=False
