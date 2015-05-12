#!/bin/bash


export FILE_NAMES="/pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_478.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_479.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_48.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_480.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_481.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_482.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_483.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_484.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_485.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_486.root "

export OUTFILE_NAME="/nfs/dust/cms/user/kelmorab/13TeV_ttHF/ttbar/MC_MadGraph_TTbar_nominal_42"

export INSAMPLE="2500"

export ERA="2015_72x"

export MAX_EVENTS="999999999"

export PU_STR="all"

export STR_DATASET="all"

export XS="831.76"

export MCEVENTS="25446993"

export SYSTEMATIC="nominal"


exec $*
