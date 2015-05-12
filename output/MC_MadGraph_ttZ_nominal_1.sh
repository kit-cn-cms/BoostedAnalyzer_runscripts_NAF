#!/bin/bash


export FILE_NAMES="/pnfs/desy.de/cms/tier2/store/user/hmildner/TTZJets_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132229/0000//BoostedTTH_MiniAOD_3.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTZJets_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132229/0000//BoostedTTH_MiniAOD_4.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTZJets_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132229/0000//BoostedTTH_MiniAOD_5.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTZJets_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132229/0000//BoostedTTH_MiniAOD_6.root "

export OUTFILE_NAME="/nfs/dust/cms/user/kelmorab/13TeV_ttHF/ttZ/MC_MadGraph_ttZ_nominal_1"

export INSAMPLE="2523"

export ERA="2015_72x"

export MAX_EVENTS="999999999"

export PU_STR="all"

export STR_DATASET="all"

export XS="2.232"

export MCEVENTS="249275"

export SYSTEMATIC="nominal"


exec $*
