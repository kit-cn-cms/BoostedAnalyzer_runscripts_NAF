outpath='/nfs/dust/cms/user/mwassmer/DarkMatter/ntuples/' # path of output of analyzer
scriptpath='MonoJet' # folder containing shell scripts that will have to be run on cluster
samplelist='../MonoJet.csv' # samples list
dataset_column='dataset' # run on the column with dataset or boosted_dataset?
cmsswcfgpath='/nfs/dust/cms/user/mwassmer/DarkMatter/CMSSW_8_0_26_patch2/src/BoostedTTH/BoostedAnalyzer/test/DarkMatter_cfg_v3.py'
cmsswpath='/nfs/dust/cms/user/mwassmer/DarkMatter/CMSSW_8_0_26_patch2/'
dbs="prod/global" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=50000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='systematicVariations_none.txt'
nSystematicVariationsPerJob=5
