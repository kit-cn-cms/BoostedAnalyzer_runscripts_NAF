# BoostedAnalyzer_runscripts_NAF  
some runscripts for usage on the NAF and other useful scripts  

Current Instructions:

## Preparation
### Prepare Samplelists
Todo

### Prepare Scripts and run them on batch system
1. Adjust a config to your needs
    * Look at configs/user_config_legacy_2017.py
    * Adjust everything to your needs
    * Adjust the outpath: This directory needs to exist
2. Prepare actual scripts
    * cd into jobTools
    * make sure you hava a valid VOMS proxy:  
        ```voms-proxy-init -rfc --voms cms:/cms/dcms --valid 72:0```
    * run  
        ``` python generate_scripts.py ../configs/user_config_legacy_2017.py ```
    * have a look at `workdir`: There should be the output
3. Submit jobs batchwise to NAF
    * cd into your project folder in the workdir
    * submit Jobs for desired sample with  
        ```../../jobTools/NAFSubmit.py ```
      * run  
        ```python ../../jobTools/NAFSubmit.py -f DESIREDSAMPLE -o jobs -M 4000 -r 800 -n DESIREDSSAMPLE```
      * Hint: might be useful to use a for loop:   
      ```for sample in *; do python ../../jobTools/NAFSubmit.py -f $sample -o jobs -M 4000 -r 800 -n $sample; done```
4. Wait for jobs to be finished
5. Check if every Job ran successful


### Check output and resubmit broken jobs
After a batch of jobs has finished you should check if alle jobs run successfully. To do so use the following instructions:
1. Find broken ROOT files:
    * run `python jobTools/findCorruptFiles.py /path/to/ntuple/folder/of/sample/to/be/checked
    * This will create a file called `broken_files.txt`
2. Delete the broken files:
    * run `python jobTools/deleteNtuples.py -f broken_files.txt`
3. Check the output to find out which jobs failed:
     * run  
       ```python jobTools/check_files.py -f BASEPATHtoNUTPLEFOLDER -s BASEPATHtoSCRIPTSFolder -n N_SYSTSPERJOB SAMPLE1 SAMPLE2 ```
     * wildcards are for samples to check
     * use `--nominal` flag for data or nominal ntuples
     * make sure your samplename matches with the scriptfolder and and foldername in ntuple directory 
     * This will create a file called `scriptsToRerun.txt`
     * Hint: It might be useful to check, why certain jobs failed, e.g. too mich memory consumption or too long runtime
4. Resubmit failed jobs:
     * use NAFSubmit.py to resubmit broken jobs via the `--file file` option
     * e.g.: cd into appropriate workdir to keep track of all your jobs and run  
       ```python ../../../jobTools/NAFSubmit.py --file ../../../scriptsToRerun.txt -o rerun1 -n SAMPLE_rerun1 -M 4000 -r 800```
5. Repeat until all jobs ran successfully
6. Profit



