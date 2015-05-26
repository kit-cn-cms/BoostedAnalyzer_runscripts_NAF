# BoostedAnalyzer_runscripts_NAF
some runscripts for usage on the NAF and other useful scripts

Instructions:

1) modify "execute.sh" to your needs

2) specify the input samples, xs and output directories in "getAllFiles.sh"
   - You should use different output directories for samples which you want to use seperately later on 
     - and the same directories if you want to combine the samples
   - e.g. tth ->tth, WW+WZ+ZZ ->DiBoson, ...
   - Make sure the directories exist

3) start the jobs with "runAll.sh"

4) After the jobs are finished do "makeTreesReady.py"
   - checks if the output files exist and makes resubmit ready if necessary
   - This will hadd all the trees in the different directories
   - discriminates between nominal and JESUP/JESDOWN samples
   - merges the cutflows 
   - makes nicer cutflow tables
   - writes AnalysisLog.txt for later use
   - collects used software and makes tarball of it
