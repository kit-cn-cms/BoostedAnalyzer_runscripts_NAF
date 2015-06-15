#!/bin/bash

INSAMPLE="9125" #TTH125
#INSAMPLE="2500" #TTbarIncl
ERA="2015_72x" #Current Era
MAX_EVENTS="999999999" 
PU_STR="all" # used for PU reweighting, not sure what it does "2012A_13July,2012A_06Aug,2012B_13July,2012C_PR,2012C_24Aug,2012D_PR"
STR_DATASET="all" # dont know where this is used
#SAMPLE_NAME="TTH_Inclusive_M_125_8TeV_53xOn53x"
OUTFOLDER_NAME="/nfs/dust/cms/user/kelmorab/test/"
#OUTFOLDER_NAME="/storage/9/mildner/BNtrees/"


FILEDIR=$1
OUTFOLDER_NAME=$2
NAME=$3
INSAMPLE=$4
XS=$5
MCEVENTS=$6
NFILES=$7
SYSTEMATIC=$8

COUNTER=0
NUMBER=0

PATTERN1="root"
PATTERN2="root~"
PATTERN3="ttbar"
PATTERN4="JetsToLNu"
PATTERN5="JetsToLL"
PATTERN6="miniaod_"


for i in `ls -1 $FILEDIR/* | grep $PATTERN1 | grep $PATTERN6 | grep -v $PATTERN2 | grep -v -f blacklist.txt `
do
	FILE=output/${NAME}_${SYSTEMATIC}_${NUMBER}

	if [ "$COUNTER" = 0 ]
	then
		echo -e '#!/bin/bash\n\n' > ${FILE}.sh
		echo -e ${FILE}.sh >> output/sampleListe${SYS}.txt
		echo -en 'export FILE_NAMES="' >> ${FILE}.sh
	fi

	echo -en $i" " >> ${FILE}.sh
	((COUNTER+=1))

	if [ "$COUNTER" = $NFILES ]
	then
		echo -e '"\n\nexport OUTFILE_NAME="'${OUTFOLDER_NAME}'/'${NAME}'_'${SYSTEMATIC}'_'${NUMBER}'"' >> ${FILE}.sh
		echo -e '\nexport INSAMPLE="'${INSAMPLE}'"' >> ${FILE}.sh
		echo -e '\nexport ERA="'${ERA}'"' >> ${FILE}.sh
		echo -e '\nexport MAX_EVENTS="'${MAX_EVENTS}'"' >> ${FILE}.sh
		echo -e '\nexport PU_STR="'${PU_STR}'"' >> ${FILE}.sh
		echo -e '\nexport STR_DATASET="'${STR_DATASET}'"' >> ${FILE}.sh
		echo -e '\nexport XS="'${XS}'"' >> ${FILE}.sh
		echo -e '\nexport MCEVENTS="'${MCEVENTS}'"' >> ${FILE}.sh
		echo -e '\nexport SYSTEMATIC="'${SYSTEMATIC}'"' >> ${FILE}.sh
#		echo -e '\nexport SAMPLE_NAME="'${SAMPLE_NAME}'"' >> ${FILE}.sh

		echo -e '\n\nexec $*' >> ${FILE}.sh

		chmod +x ${FILE}.sh

		COUNTER=0
		((NUMBER+=1))
	fi

done

if [ "$COUNTER" -ne 0 ]
then
		echo -e '"\n\nexport OUTFILE_NAME="'${OUTFOLDER_NAME}'/'${NAME}'_'${SYSTEMATIC}'_'${NUMBER}'"' >> ${FILE}.sh
		echo -e '\nexport INSAMPLE="'${INSAMPLE}'"' >> ${FILE}.sh
		echo -e '\nexport ERA="'${ERA}'"' >> ${FILE}.sh
		echo -e '\nexport MAX_EVENTS="'${MAX_EVENTS}'"' >> ${FILE}.sh
		echo -e '\nexport PU_STR="'${PU_STR}'"' >> ${FILE}.sh
		echo -e '\nexport STR_DATASET="'${STR_DATASET}'"' >> ${FILE}.sh
		echo -e '\nexport XS="'${XS}'"' >> ${FILE}.sh
		echo -e '\nexport MCEVENTS="'${MCEVENTS}'"' >> ${FILE}.sh
		echo -e '\nexport SYSTEMATIC="'${SYSTEMATIC}'"' >> ${FILE}.sh
#		echo -e '\nexport SAMPLE_NAME="'${SAMPLE_NAME}'"' >> ${FILE}.sh

		echo -e '\n\nexec $*' >> ${FILE}.sh

		chmod +x ${FILE}.sh

fi
