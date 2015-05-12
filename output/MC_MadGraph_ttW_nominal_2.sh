#!/bin/bash


export FILE_NAMES="/pnfs/desy.de/cms/tier2/store/user/hmildner/TTWJets_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132213/0000//BoostedTTH_MiniAOD_9.root "

export OUTFILE_NAME="/nfs/dust/cms/user/kelmorab/13TeV_ttHF/ttW/MC_MadGraph_ttW_nominal_2"

export INSAMPLE="2524"

export ERA="2015_72x"

export MAX_EVENTS="999999999"

export PU_STR="all"

export STR_DATASET="all"

export XS="1.152"

export MCEVENTS="246521"

export SYSTEMATIC="nominal"


exec $*
