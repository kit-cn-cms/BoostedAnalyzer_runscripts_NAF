#!/bin/bash


export FILE_NAMES="/pnfs/desy.de/cms/tier2/store/user/hmildner/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/BoostedTTH_MiniAOD/150509_134128/0000//BoostedTTH_MiniAOD_6.root "

export OUTFILE_NAME="/nfs/dust/cms/user/kelmorab/13TeV_ttHF/tth/MC_aMCatNLO_TTH_nominal_5"

export INSAMPLE="9125"

export ERA="2015_72x"

export MAX_EVENTS="999999999"

export PU_STR="all"

export STR_DATASET="all"

export XS="0.5085"

export MCEVENTS="93694"

export SYSTEMATIC="nominal"


exec $*
