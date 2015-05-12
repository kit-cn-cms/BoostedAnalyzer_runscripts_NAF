#!/bin/bash


export FILE_NAMES="/pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_414.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_415.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_416.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_417.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_418.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_419.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_42.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_420.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_421.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_422.root "

export OUTFILE_NAME="/nfs/dust/cms/user/kelmorab/13TeV_ttHF/ttbar/MC_MadGraph_TTbar_nominal_35"

export INSAMPLE="2500"

export ERA="2015_72x"

export MAX_EVENTS="999999999"

export PU_STR="all"

export STR_DATASET="all"

export XS="831.76"

export MCEVENTS="25446993"

export SYSTEMATIC="nominal"


exec $*
