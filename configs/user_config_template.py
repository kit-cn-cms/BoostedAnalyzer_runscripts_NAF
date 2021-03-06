outpath='/aaa/bbb/ccc/' # path of output of analyzer, so where the ntuples will be. This path has to exist, so create it!
scriptpath='folder_where_scripts_will_be' # folder (relative or aboluste path) containing shell scripts that will have to be run on cluster, e.g. htcondor
samplelist='your_sample_list.csv' # path to csv sample list (relative or absolute path)
dataset_column='dataset' # run on the column (in the csv file above) with dataset or boosted_dataset?
cmsswcfgpath='/path/to/your/cmsRun/config.py' # this is the path to the cmssw python config which tells cmssw what to do
cmsswpath='/path/to/cmssw/installation/CMSSW_X_Y_Z/' # path to be the base directory of the cmssw installtion you want to use
dbs="prod/phys03" # dbs instance: self-created samples (like skims or slims) are in prod/phys03, standard miniaod from global production in prod/global
min_events_per_job=50000 # min number of events per job which will be processed 
isBoostedMiniAOD=False # do the inputs contain fat jets? (deprecated at the moment)
systematicVariations='systematicVariations.txt'# path to a .txt file with a list of JEC sources. The ntuples will also be produced for these JEC variations 
nSystematicVariationsPerJob=4 # number of JEC sources which one BoostedAnalyzer job will process
ProduceMemNtuples=False # special flag to produce ntuples which serve as input to MEM calculation
