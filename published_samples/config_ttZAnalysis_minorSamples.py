outpath='/nfs/dust/cms/user/vdlinden/ttZAnalysis/' # path of output of analyzer
scriptpath='ttZAnalysis_minorSamples' # folder containing shell scripts that will have to be run on cluster
samplelist='../samples_ttZAnalysis_minorBkgs.csv' # samples list
dataset_column='boosted_dataset' # run on the column with dataset or boosted_dataset?
cmsswcfgpath='/nfs/dust/cms/user/vdlinden/ttZAnalysis/CMSSW_ntupling/CMSSW_10_2_13/src/BoostedTTH/BoostedAnalyzer/test/ntupling_ttZAnalysis.py'
cmsswpath='/nfs/dust/cms/user/vdlinden/ttZAnalysis/CMSSW_ntupling/CMSSW_10_2_13/'
dbs="prod/phys03" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=100000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='systematics_ttZAnalysis.txt'
nSystematicVariationsPerJob=3
ProduceMemNtuples=False
