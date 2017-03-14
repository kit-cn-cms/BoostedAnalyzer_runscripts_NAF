outpath='/nfs/dust/cms/user/kelmorab/trees_Spring17_v2' # path of output of analyzer
scriptpath='runScripts_Spring17-v2_ttbarSL' # folder containing shell scripts that will have to be run on cluster
samplelist='SampleListSpring17_ttbarSL.csv' # samples list
dataset_column='boosted_dataset' # run on the column with dataset or boosted_dataset?
cmsswcfgpath='/nfs/dust/cms/user/kelmorab/CMSSW_Moriond2017/CMSSW_8_0_26_patch1/src/BoostedTTH/BoostedAnalyzer/test/boostedAnalysis_ntuples-Spring17_cfg.py'
cmsswpath='/nfs/dust/cms/user/kelmorab/CMSSW_Moriond2017/CMSSW_8_0_26_patch1/'
dbs="prod/phys03" # dbs instance: boosted miniaod is in prod/phys03, standard miniaod in prod/global
min_events_per_job=50000 # min number of events per job 
isBoostedMiniAOD=False # do the inputs contain fat jets?
systematicVariations='systematicVariations.txt'
nSystematicVariationsPerJob=6
