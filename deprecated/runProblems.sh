for i in `cat output/sampleListe_Problems.txt`
  do 
  INPUTSCRIPT=$i
  export INPUTSCRIPT 
  qsub -l h=bird* -hard -l os=sld6 -l h_vmem=2000M -l s_vmem=2000M -cwd -S /bin/bash -v INPUTSCRIPT -N `basename $i .sh` -o logs/\$JOB_NAME.o\$JOB_ID -e logs/\$JOB_NAME.e\$JOB_ID -q 'default.q' execute.sh
done
