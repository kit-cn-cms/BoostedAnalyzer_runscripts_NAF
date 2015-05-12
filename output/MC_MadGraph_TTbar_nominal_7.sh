#!/bin/bash


export FILE_NAMES="/pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_162.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_163.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_164.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_165.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_166.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_167.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_168.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_169.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_17.root /pnfs/desy.de/cms/tier2/store/user/hmildner/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/BoostedTTH_MiniAOD/150509_132153/0000//BoostedTTH_MiniAOD_170.root "

export OUTFILE_NAME="/nfs/dust/cms/user/kelmorab/13TeV_ttHF/ttbar/MC_MadGraph_TTbar_nominal_7"

export INSAMPLE="2500"

export ERA="2015_72x"

export MAX_EVENTS="999999999"

export PU_STR="all"

export STR_DATASET="all"

export XS="831.76"

export MCEVENTS="25446993"

export SYSTEMATIC="nominal"


exec $*
