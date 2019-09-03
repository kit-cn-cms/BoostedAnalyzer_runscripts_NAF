* create a sample list containing all samples you want to analyze (just add or delete lines in the csv files in this folder)
* copy and edit `user_config.py` (see comments in file) 
* generate scripts with `./generate_scripts.py user_config_name.py`

* move to generated directory 
* submit scripts to cluster from directory created by `.generate_scripts.py`
```
python ../NAFSubmit.py -f $dir -o submit -n $dir
```
* wait until all jobs finished

* move to generated directory/submit
* check which jobs have not finished
* `python ../../find_broken_files.py --name=DIRNAME BASEPATHTONTUPLES/DIRNAME

* move to generated directory/submit
* resubmit broken files
* `python ../../find_broken_shells.py -j ../joblist.txt -p ../../ -b DIRNAME_broken_files.txt -d ../resubmit -n resubmit_DIRNAME --submit`
