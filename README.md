# BoostedAnalyzer_runscripts_NAF  
some runscripts for usage on the NAF and other useful scripts  

Current Instructions:

## Preparation
### Prepare Samplelists
Todo

### Prepare Script to be run on batch system
1. Adjust a config to your needs
  * Look at configs/user_config_legacy_2017.py
  * Adjust everything to your needs
  * Adjust the outpath: This directory needs to exist
2. Prepare actual scripts
  * cd into jobTools
  * make sure you hava a valid VOMS proxy: ```voms-proxy-init -rfc --voms cms:/cms/dcms --valid 72:0```
  * run ``` python generate_scripts.py ../configs/user_config_legacy_2017.py ```
  * have a look at `workdir`: There should be the output
3. Submit jobs batchwise to NAF
  * cd into your project folder in the workdir
  * submit Jobs for desired sample with ```../../jobTools/NAFSubmit.py ```
    * ```python ../../jobTools/NAFSubmit.py -f DESIREDSAMPLE -o jobs -M 4000 -r 800 -n DESIREDSSAMPLE```
    * Hint: might be useful to use a for loop: 
      ```for sample in *; do python ../../jobTools/NAFSubmit.py -f $sample -o jobs -M 4000 -r 800 -n $sample; done```
4. Wait for jobs to be finished
5. Check if every Job ran successful
  * TODO EXPLAIN HOW TO CHECK and resubmit




Tragically outdated Instructions:

#### 1)
modify "execute.sh" to your needs  
e.g. change paths to you CMSSW and cwd and the cmsRun python config you want to use
the config already implemented should work fine


#### 2)
look at "getAllFiles.sh"  
specify  
- input samples
- output directory
- Sample id ( doesn't really matter at the moment )
- XS
- number of MC in sample ( can be counted with "GetTotalSampleNumbers.py" which takes either a list of MiniAOD.root files or a DAS query as input)
- number of input files per job

this will prepare the input scripts for the batch system  
- You should use different output directories for samples which you want to use seperately later on   
   - and the same directories if you want to combine the samples  
- e.g. tth ->tth, WW+WZ+ZZ ->DiBoson, ...  
- Make sure the directories exist  

#### 3)
  start the jobs with "runAll.sh"  

#### 4)
After the jobs are finished do "makeTreesReady.py"  
   - checks if the output files exist and makes resubmit ready if necessary  
   - This will hadd all the trees in the different directories  
   - differentiates between nominal and JESUP/JESDOWN samples  
   - merges the cutflows   
   - makes nicer cutflow tables  
   - writes AnalysisLog.txt for later use  
   - collects used software and makes tarball of it  

You can merge the cutflow files with "merge_cutflow.py"  and create a nice table with "makeYieldTables.py"  

