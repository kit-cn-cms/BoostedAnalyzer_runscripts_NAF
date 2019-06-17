* create a sample list containing all samples you want to analyze (just add or delete lines in the csv files in this folder)
* copy and edit user_config.py (see comments in file) 
* generate scripts with './generate_scripts.py user_config_name.py'
* submit scripts to cluster with ./sup.py -f folder_with_scripts
* qstat and wait until all jobs finished
* './check_jobs.py scriptsfolder/joblist.txt' will tell you which jobs did not finish successfully
* resubmit jobs with ./sup.py names of scripts that failed (e.g. ./sup.py scriptsfolder/ttbar/ttbar_13.sh scriptsfolder/tth/tth_51.sh)
